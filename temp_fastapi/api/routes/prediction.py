from datetime import datetime,timedelta
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException,status
from models.prediction import TemperaturePrediction
from models.payload import TemperaturePredictionPayload
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError,jwt
from enum import Enum
from passlib.context import CryptContext

router = APIRouter()

#set model types available to user
class ModelType(str,Enum):
    RF='random_forest'
    SVR='support_vector'
    LGBM='lightgbm'

SECRET_KEY='44e64a8acf69d36a3009c43e943d092fdc8967e19e262a41da46b133f2db3bad'
ALGORITHM='HS256'
TOKEN_EXPIRE_TIME=30


class Token(BaseModel):
    token: str
    toke_type: str

class Roles(str, Enum):
    RESEARCHER='researcher'
    PM='product manager'
    DS='data scientists'
    STUDENT='student'


class TokenData(BaseModel):
    username: str| None = None

user_db={
    "imma": {
        "username": 'imma_mnene',
        "role": Roles.PM,
        "hashed_password": "$2b$12$Q8iK7SvvTYFeoF5ZBfg9W.dU4RsB7IYHzflrs7pGKUNGwEEclyilW",
        "disabled": False

    }
}


class User(BaseModel):
    username: str
    role: Roles|None= None
    disabled: bool|None=None


class UserInDB(User):
    hashed_password: str


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')

pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

async def get_user(user_db,username: str):
    if username in user_db:
        user_dict=user_db[username]
        return UserInDB(**user_dict)
    

def hash_pasword(password: str):
    pwd_context.hash(password)


def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)


def authenticate_user(user_db,username: str, password: str):
    user=get_user(user_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_pasword):
        return False
    return user


def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Credentials could not be validated',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data=TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    user=get_user(user_db,username)
    if user is None:
        raise credentials_exception
    
    return user
    

def create_token(data: dict,expire_delta: timedelta| None= None):
    to_encode=data.copy()
    if expire_delta:
        expire=datetime.utcnow()+expire_delta
    else:
        expire=datetime.utcnow()+timedelta(5)
    
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/token',response_model=Token)
def token_gen(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=authenticate_user(user_db=user_db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login data',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires=timedelta(minutes=TOKEN_EXPIRE_TIME)
    token=create_token(data={"sub": user.username}, expire_delta=access_token_expires)
    return {'access token': token, 'token type': 'Bearer'}


#run predction at endpoint from the FastAPI app object
@router.post("/model_deploy/{model_type}",
             response_model= TemperaturePrediction)
async def predict(request: Request,model_type: ModelType,
                  payload: TemperaturePredictionPayload) -> TemperaturePrediction:     
       
    if model_type==ModelType.RF:
        model = request.app.state.model_rf
    elif model_type==ModelType.SVR:
        model = request.app.state.model_svr
    else:
        model = request.app.state.model_lgbm
    prediction: TemperaturePrediction = model.predict(payload)
    return prediction
