"""
Authentication service for GES application
Handles user authentication and authorization
"""

import hashlib
from typing import Optional
from app.repositories.user_repository import UserRepository
from database.models.person import UserModel


class AuthService:
    """Service for user authentication and management"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[UserModel]:
        """Authenticate user with username and password"""
        if not username or not password:
            return None
        
        password_hash = self.hash_password(password)
        user = self.user_repo.authenticate(username, password_hash)
        
        if user:
            # Update last login
            self.user_repo.update_last_login(user.id)
        
        return user
    
    def create_user(self, username: str, password: str, role: str, person_id: Optional[int] = None) -> UserModel:
        """Create new user with validation"""
        # Validate input
        if not username or not password or not role:
            raise ValueError("Username, password, and role are required")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        # Check if username already exists
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Create user
        password_hash = self.hash_password(password)
        
        user = UserModel(
            username=username,
            password_hash=password_hash,
            role=role,
            person_id=person_id
        )
        
        return self.user_repo.create(user)
    
    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username"""
        return self.user_repo.get_by_username(username)
    
    def is_valid_role(self, role: str) -> bool:
        """Validate user role"""
        from database.models.person import UserRole
        valid_roles = [UserRole.ADMIN.value, UserRole.SECRETARY.value, UserRole.TEACHER.value]
        return role in valid_roles
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters")
        
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        # Verify old password
        old_password_hash = self.hash_password(old_password)
        if user.password_hash != old_password_hash:
            return False
        
        # Update password
        user.password_hash = self.hash_password(new_password)
        self.user_repo.update(user)
        return True
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self.user_repo.update(user)
        return True
