from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

DATABASE_URL = "sqlite:///ges_database.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Get database session"""
    return SessionLocal()


def close_session(session):
    """Close database session"""
    session.close()
