from datetime import timedelta
from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

#from db.user_schemas import Token ,response_model=Token
from api.db.user_schemas import Token
from core.auth import authenticate_user,signup_user
from core.security import TOKEN_EXPIRATION,create_access_token
from api.db.session import Base,engine,get_db
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)


router=APIRouter()


@router.post('/token',response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                db: Annotated[Session,Depends(get_db)]):
    user= authenticate_user(db=db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate':'Bearer'}
        )
    access_token_expiry=timedelta(seconds=TOKEN_EXPIRATION)
    access_token=create_access_token(
        data={'sub':user.username},
        expires_delta=access_token_expiry
    )

    return {'access_token': access_token,'token_type': 'bearer'}


@router.post('/signup',response_model=Token)
async def signup(db: Annotated[Session,Depends(get_db)],
                 form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=signup_user(
        db,username=form_data.username,
        password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with that mail already exists',
            headers={'WWW-Authenticate':'Bearer'}
        )
    access_token_expiry=timedelta(minutes=TOKEN_EXPIRATION)
    access_token=create_access_token(
        data={'sub':user.username},expires_delta=access_token_expiry
    )
    return {'access_token': access_token,'token_type': 'bearer'}


