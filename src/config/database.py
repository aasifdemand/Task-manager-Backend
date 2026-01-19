from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.config import DATABASE_URL
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Generator

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,# avoids stale connections
    echo=True   
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
