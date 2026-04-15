from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base




SQL_URL = 'sqlite:///db.db'
engine  = create_engine(SQL_URL,echo=True)
SessionLocal = sessionmaker(autoflush=False,bind=engine,expire_on_commit=False)

Base  = declarative_base()



def  get_db():
    db =  SessionLocal()
    try:
        yield db 

    finally:
        db.close()