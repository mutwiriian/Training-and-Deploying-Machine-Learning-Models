from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta


pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY='f3cdf59b55ef5473df51f2239e7f7623b0dff11182388e5ac409053899af56cc'
ALGORITHM='HS256'
TOKEN_EXPIRATION=10


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=5)

    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt