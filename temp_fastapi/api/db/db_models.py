from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .session import Base


class User(Base):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    username: Mapped[str]
    hashed_password: Mapped[str]


