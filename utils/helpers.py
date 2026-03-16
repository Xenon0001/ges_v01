"""
Utils - Helper functions compartidos
Funciones utilitarias usadas por UI y API
"""

import hashlib
import secrets

def hash_password(password: str) -> str:
    """
    Hashea password usando SHA-256 (sin salt para MVP)
    Mantiene compatibilidad con usuarios existentes
    """
    return hashlib.sha256(password.encode()).hexdigest()

def generate_simple_token(length: int = 32) -> str:
    """
    Genera token simple alfanumérico
    """
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))
