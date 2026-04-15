from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use DATABASE_URL from environment, fallback to SQLite for development
DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///db.db')

# For PostgreSQL URLs that come from Render with the old psycopg2 driver
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL, echo=True,pool_pre_ping=True,pool_recycle=300)
SessionLocal = sessionmaker(autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db 

    finally:
        db.close()