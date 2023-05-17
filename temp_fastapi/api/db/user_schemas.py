from pydantic import BaseModel


class UserBase(BaseModel):
    username: str| None = None


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode=True


class User(UserBase):
    id: int

    class Config:
        orm_mode=True
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str