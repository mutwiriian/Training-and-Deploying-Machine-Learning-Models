from pydantic import  BaseModel, EmailStr
from enum import Enum

class Tier(int,Enum):
    TIER_1=1
    TIER_2=2
    TIER_3=3


class User(BaseModel):
    user_name: set
    email: EmailStr
    pass_word: str
    tier: Tier




