"""
Dashboard Routes - Métricas y Datos del Dashboard
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime

from services.academic_service import AcademicService
from services.finance_service import FinanceService
from api.auth_manager import get_current_user

router = APIRouter()

academic_service = AcademicService()
finance_service = FinanceService()

@router.get("/")
async def get_dashboard_data(current_user: Dict = Depends(get_current_user)):
    """
    Obtiene datos del dashboard
    Requiere token válido
    """
    try:
        # Cargar datos académicos
        academic_data = academic_service.get_academic_dashboard_data(2024)
        
        # Cargar datos financieros
        financial_data = finance_service.get_financial_dashboard_data()
        
        return {
            "academic": academic_data,
            "financial": financial_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error obteniendo datos del dashboard")
