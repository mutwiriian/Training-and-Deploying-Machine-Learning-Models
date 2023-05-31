from . import db_models
from .user_schemas import UserCreate
from core.security import get_password_hash

from sqlalchemy import select
from sqlalchemy.orm import Session


def get_user_by_username(db: Session, username: str):
    stmt=select(db_models.User).where(db_models.User.username==username)
    return db.scalars(stmt).first()


def create_user(db: Session,user: UserCreate):
    hashed_password=get_password_hash(user.password)
    db_user=db_models.User(username=user.username,
                           hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


