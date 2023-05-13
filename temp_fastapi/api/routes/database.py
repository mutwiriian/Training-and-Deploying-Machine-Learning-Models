from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine=create_engine('postgresql+psycopg2://ian:quant@localhost:8080/users')

SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base=DeclarativeBase()

