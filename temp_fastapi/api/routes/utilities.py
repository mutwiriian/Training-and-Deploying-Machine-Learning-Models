from sqlalchemy.orm import Session

from . import model,schema

def get_user(db: Session,user_id: int):
    db.query(model.User).filter(model.User.id==user_id).first()

def create_user(db: Session,user: schema.UserCreate):
    hashed_password= 