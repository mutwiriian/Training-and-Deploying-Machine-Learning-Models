from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine=create_engine('sqlite:///./sql_app.db')
#postgresql+psycopg2://ian:quant@localhost:8080/users

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()