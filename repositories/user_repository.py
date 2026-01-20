from typing import Optional
from database.models.person import UserModel
from .base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self):
        super().__init__(UserModel)
    
    def get_by_username(self, username: str) -> Optional[UserModel]:
        session = self.get_session()
        try:
            return session.query(UserModel).filter(UserModel.username == username).first()
        finally:
            self.close()
    
    def authenticate(self, username: str, password_hash: str) -> Optional[UserModel]:
        session = self.get_session()
        try:
            return session.query(UserModel).filter(
                UserModel.username == username,
                UserModel.password_hash == password_hash,
                UserModel.is_active == True
            ).first()
        finally:
            self.close()
