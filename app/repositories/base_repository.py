"""
Base repository for all GES repositories
Provides common CRUD operations
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Type
from database.db import get_db
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def get_session(self) -> Session:
        """Get database session"""
        return next(get_db())
    
    def create(self, entity: T) -> T:
        """Create new entity"""
        session = self.get_session()
        try:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity
        except Exception:
            session.rollback()
            raise
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        session = self.get_session()
        try:
            return session.query(self.model_class).filter(self.model_class.id == entity_id).first()
        finally:
            pass  # Session managed by context manager
    
    def get_all(self) -> List[T]:
        """Get all entities"""
        session = self.get_session()
        try:
            return session.query(self.model_class).all()
        finally:
            pass  # Session managed by context manager
    
    def update(self, entity: T) -> T:
        """Update entity"""
        session = self.get_session()
        try:
            session.merge(entity)
            session.commit()
            session.refresh(entity)
            return entity
        except Exception:
            session.rollback()
            raise
    
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID"""
        session = self.get_session()
        try:
            entity = session.query(self.model_class).filter(self.model_class.id == entity_id).first()
            if entity:
                session.delete(entity)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            raise
