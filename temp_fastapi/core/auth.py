from fastapi import Depends,HTTPException,status
from api.db.crud import get_user_by_username,create_user
from core.security import SECRET_KEY,ALGORITHM,oauth2_scheme,verify_password
from api.db.user_schemas import TokenData,UserCreate
from jose import jwt,JWTError
from api.db.session import get_db


async def get_current_user(token= Depends(oauth2_scheme),db = Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data=TokenData(username=username)

    except JWTError:
        raise credentials_exception
    user=get_user_by_username(db,username=token_data.username)
    return user


def authenticate_user(db,username: str, password: str):
    user=get_user_by_username(db=db,username=username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user


def signup_user(db,username: str,password: str):
    user = get_user_by_username(db=db,username=username)
    if user:
        return False
    new_user=create_user(
        db,UserCreate(
        username=username,
        password=password)
        )
    
    return new_user











