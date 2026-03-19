"""
GES - Sistema de Gestión Escolar
Configuración principal del proyecto
"""

import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ges.db"

# Configuración servidor
DEFAULT_PORT = 8000
HOST = "0.0.0.0"

# Nombres de tablas
TABLES = {
    "schools": "schools",
    "users": "users", 
    "roles": "roles",
    "levels": "levels",
    "grades": "grades",
    "classrooms": "classrooms",
    "enrollment_prices": "enrollment_prices",
    "subjects": "subjects",
    "teachers": "teachers",
    "students": "students",
    "scores": "scores",
    "payments": "payments",
    "alerts": "alerts",
    "history": "history"
}

# Asegurar directorio de datos
os.makedirs(DATA_DIR, exist_ok=True)
