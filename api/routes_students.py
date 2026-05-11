"""
Students Routes - Gestión de Estudiantes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

from services.student_service import StudentService
from api.auth_manager import get_current_user

router = APIRouter()

# Modelos Pydantic
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    tutor_name: str
    classroom_id: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    tutor_name: str
    classroom_id: Optional[int]
    created_at: datetime

student_service = StudentService()

@router.get("/", response_model=List[StudentResponse])
async def get_students(current_user: Dict = Depends(get_current_user)):
    """
    Lista todos los estudiantes
    Requiere token válido
    """
    try:
        students = student_service.get_all_students()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error obteniendo estudiantes")

@router.post("/", response_model=StudentResponse)
async def create_student(
    student: StudentCreate, 
    current_user: Dict = Depends(get_current_user)
):
    """
    Crea nuevo estudiante
    Requiere token válido y permisos
    """
    try:
        # Validar permisos (solo Secretaria o Directiva)
        if current_user.get('role_id') not in [1, 2]:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        
        student_data = student.dict()
        new_student = student_service.create_student(student_data)
        return new_student
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creando estudiante")
