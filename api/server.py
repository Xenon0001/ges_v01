"""
GES API Server - Modo Servidor LAN
FastAPI server para acceso remoto a GES
"""

import sys
import os
from pathlib import Path

# Agregar directorio raíz al path para imports relativos
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Import de routes (sin importación circular)
from api.routes_auth import router as auth_router
from api.routes_students import router as students_router
from api.routes_dashboard import router as dashboard_router
from api.auth_manager import cleanup_expired_tokens

# Configuración
app = FastAPI(
    title="GES API",
    description="API para Sistema de Gestión Escolar",
    version="1.0.0"
)

# Middleware CORS para LAN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Incluir routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(students_router, prefix="/students", tags=["students"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

# Health check
@app.get("/health")
async def health_check():
    cleanup_expired_tokens()  # Limpieza periódica
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
