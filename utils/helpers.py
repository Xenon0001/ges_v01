"""
Utils - Helper functions compartidos
Funciones utilitarias usadas por UI y API
"""

import hashlib
import secrets
import unicodedata
import re
from typing import Any

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


def normalize_text(value: Any) -> str:
    """Normaliza texto para comparación robusta."""
    if value is None:
        return ''
    text = str(value).strip()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def normalize_enrollment_number(value: Any) -> str:
    """Normaliza el número de matrícula eliminando símbolos y espacios."""
    text = normalize_text(value)
    return re.sub(r'[^a-z0-9]', '', text)


def normalize_classroom_name(value: Any) -> str:
    """Normaliza nombres de curso/aula para evitar variantes comunes."""
    text = normalize_text(value)
    if not text:
        return ''

    ordinal_map = {
        'primero': '1',
        'primera': '1',
        'segundo': '2',
        'segunda': '2',
        'tercero': '3',
        'tercera': '3',
        'cuarto': '4',
        'cuarta': '4',
        'quinto': '5',
        'quinta': '5',
        'sexto': '6',
        'sexta': '6'
    }

    for word, number in ordinal_map.items():
        text = re.sub(rf'\b{word}\b', number, text)

    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.replace(' ', '')
