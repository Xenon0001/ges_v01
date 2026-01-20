"""
User repository for GES application
Handles user-related data operations
"""

from typing import Optional
from database.models.person import UserModel, PersonModel
from .base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """Repository for User operations"""
    
    def __init__(self):
        super().__init__(UserModel)
    
    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username"""
        session = self.get_session()
        try:
            return session.query(UserModel).filter(UserModel.username == username).first()
        finally:
            pass  # Session managed by context manager
    
    def authenticate(self, username: str, password_hash: str) -> Optional[UserModel]:
        """Authenticate user with username and password hash"""
        session = self.get_session()
        try:
            return session.query(UserModel).filter(
                UserModel.username == username,
                UserModel.password_hash == password_hash,
                UserModel.is_active == True
            ).first()
        finally:
            pass
    
    def get_by_role(self, role: str) -> list:
        """Get users by role"""
        session = self.get_session()
        try:
            return session.query(UserModel).filter(UserModel.role == role).all()
        finally:
            pass
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        session = self.get_session()
        try:
            user = session.query(UserModel).filter(UserModel.id == user_id).first()
            if user:
                from datetime import datetime
                user.last_login = datetime.utcnow()
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            pass


class PersonRepository(BaseRepository[PersonModel]):
    """Repository for Person operations"""
    
    def __init__(self):
        super().__init__(PersonModel)
    
    def get_by_email(self, email: str) -> Optional[PersonModel]:
        """Get person by email"""
        session = self.get_session()
        try:
            return session.query(PersonModel).filter(PersonModel.email == email).first()
        finally:
            pass
    
    def search_by_name(self, name: str, last_name: str = None) -> list:
        """Search persons by name"""
        session = self.get_session()
        try:
            query = session.query(PersonModel).filter(PersonModel.name.ilike(f"%{name}%"))
            if last_name:
                query = query.filter(PersonModel.last_name.ilike(f"%{last_name}%"))
            return query.all()
        finally:
            pass
