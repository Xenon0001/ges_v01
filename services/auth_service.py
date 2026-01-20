import hashlib
from typing import Optional
from repositories.user_repository import UserRepository
from database.models import UserModel


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[UserModel]:
        """Authenticate user with username and password"""
        password_hash = self.hash_password(password)
        user = self.user_repo.authenticate(username, password_hash)
        
        if user:
            # Update last login
            from datetime import datetime
            user.last_login = datetime.utcnow()
            self.user_repo.update(user)
        
        return user
    
    def create_user(self, username: str, password: str, role: str, person_id: Optional[int] = None) -> UserModel:
        """Create new user"""
        password_hash = self.hash_password(password)
        
        user = UserModel(
            username=username,
            password_hash=password_hash,
            role=role,
            person_id=person_id
        )
        
        return self.user_repo.create(user)
