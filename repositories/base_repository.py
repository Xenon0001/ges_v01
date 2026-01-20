from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Type
from sqlalchemy.orm import Session
from database.db import get_db

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self._session = None
    
    def get_session(self) -> Session:
        return next(get_db())
    
    def close(self):
        pass  # Session is managed by get_db() context manager
    
    def create(self, entity: T) -> T:
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
        session = self.get_session()
        try:
            return session.query(self.model_class).filter(self.model_class.id == entity_id).first()
        finally:
            pass  # Session will be closed by context manager
    
    def get_all(self) -> List[T]:
        session = self.get_session()
        try:
            return session.query(self.model_class).all()
        finally:
            pass  # Session will be closed by context manager
    
    def update(self, entity: T) -> T:
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
