"""
Authentication Routes - Login y Token Management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

from database.repository import user_repo
from utils.helpers import hash_password
from api.auth_manager import create_token, invalidate_token

router = APIRouter()

# Modelos Pydantic
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_data: Dict[str, Any]
    expires_at: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Autentica usuario y devuelve token
    """
    try:
        # Buscar usuario
        user = user_repo.get_by_username(request.username)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Verificar password usando helper compartido
        hashed_password = hash_password(request.password)
        if user['password_hash'] != hashed_password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Crear token usando auth_manager
        token, expires = create_token({
            "id": user['id'],
            "username": user['username'],
            "role_id": user['role_id']
        })
        
        return LoginResponse(
            token=token,
            user_data={
                "id": user['id'],
                "username": user['username'],
                "role_id": user['role_id']
            },
            expires_at=expires.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en autenticación")

@router.post("/logout")
async def logout(token: str):
    """
    Invalida token
    """
    invalidate_token(token)
    return {"message": "Sesión cerrada"}
