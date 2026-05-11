"""
Auth Manager - Gestión de autenticación
Evita importación circular entre server y routes
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Almacenamiento centralizado de tokens
active_tokens: Dict[str, Dict] = {}  # token -> {user_data, expires}

# Seguridad
security = HTTPBearer()

def create_token(user_data: Dict[str, Any]) -> tuple[str, datetime]:
    """
    Crea y guarda token, devuelve (token, expires)
    """
    from utils.helpers import generate_simple_token
    
    token = generate_simple_token()
    expires = datetime.now() + timedelta(hours=24)
    
    active_tokens[token] = {
        "user_data": user_data,
        "expires": expires
    }
    
    return token, expires

def invalidate_token(token: str) -> bool:
    """
    Invalida token, devuelve True si existía
    """
    if token in active_tokens:
        del active_tokens[token]
        return True
    return False

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Valida token y devuelve user_data
    Dependency de FastAPI para endpoints protegidos
    """
    token = credentials.credentials
    
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    token_data = active_tokens[token]
    
    # Validar expiración
    if token_data["expires"] < datetime.now():
        del active_tokens[token]
        raise HTTPException(status_code=401, detail="Token expirado")
    
    return token_data["user_data"]

def cleanup_expired_tokens():
    """
    Limpia tokens expirados (llamar periódicamente)
    """
    now = datetime.now()
    expired_tokens = [
        token for token, data in active_tokens.items()
        if data["expires"] < now
    ]
    
    for token in expired_tokens:
        del active_tokens[token]
