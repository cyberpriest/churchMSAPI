from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///db.db')

# Railway provides 'postgres://' but SQLAlchemy requires 'postgresql://'
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(
    DATABASE_URL,
    echo=True,           # logs SQL queries — change to False in production
    pool_pre_ping=True,  # prevents stale connections
    pool_recycle=300     # refreshes connections every 5 mins
)

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()