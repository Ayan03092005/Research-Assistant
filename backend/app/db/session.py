from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing import Generator
from ..config.settings import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency
def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session for FastAPI dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
