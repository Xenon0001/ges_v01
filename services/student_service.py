"""
Student Service - Orquesta operaciones de estudiantes
Combina repository y core engine para gestión de estudiantes
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from database.repository import (
    student_repo, classroom_repo, payment_repo, score_repo
)
from core.engine import CoreEngine, AcademicMetrics, FinancialMetrics, Alert, AlertType, EnrollmentStatus


class StudentService:
    """Servicio para gestión de estudiantes"""
    
    def __init__(self):
        self.student_repo = student_repo
        self.classroom_repo = classroom_repo
        self.payment_repo = payment_repo
        self.score_repo = score_repo
        self.engine = CoreEngine()
    
    def create_student(self, student_data: Dict[str, Any]) -> int:
        """Crea un nuevo estudiante con validaciones"""
        
        # Validaciones básicas
        if not student_data.get('first_name') or not student_data.get('last_name'):
            raise ValueError("Nombre y apellido son obligatorios")
        
        # Validar que el aula exista si se especifica
        if student_data.get('classroom_id'):
            classroom = self.classroom_repo.get_by_id(student_data['classroom_id'])
            if not classroom:
                raise ValueError("El aula especificada no existe")
        
        # Establecer valores por defecto
        if 'enrollment_status' not in student_data:
            student_data['enrollment_status'] = EnrollmentStatus.ACTIVO.value
        
        # Crear estudiante
        student_id = self.student_repo.create(student_data)
        
        return student_id
    
    def get_student(self, student_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un estudiante con información básica"""
        return self.student_repo.get_by_id(student_id)
    
    def update_student(self, student_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza datos de un estudiante"""
        
        # Validar que el estudiante exista
        student = self.student_repo.get_by_id(student_id)
        if not student:
            return False
        
        # Validar aula si se especifica
        if 'classroom_id' in data and data['classroom_id']:
            classroom = self.classroom_repo.get_by_id(data['classroom_id'])
            if not classroom:
                raise ValueError("El aula especificada no existe")
        
        # Actualizar
        rows_affected = self.student_repo.update(student_id, data)
        return rows_affected > 0
    
    def delete_student(self, student_id: int) -> bool:
        """Elimina un estudiante (cambia estado a retirado)"""
        
        student = self.student_repo.get_by_id(student_id)
        if not student:
            return False
        
        # En lugar de eliminar, cambiar estado
        return self.update_student(student_id, {'enrollment_status': EnrollmentStatus.RETIRADO.value})
    
    def get_students_by_classroom(self, classroom_id: int) -> List[Dict[str, Any]]:
        """Obtiene estudiantes activos de un aula"""
        students = self.student_repo.get_by_classroom(classroom_id)
        return [s for s in students if s['enrollment_status'] == EnrollmentStatus.ACTIVO.value]
    
    def search_students(self, query: str) -> List[Dict[str, Any]]:
        """Busca estudiantes por nombre o apellido"""
        return self.student_repo.search_by_name(query)
    
    def get_active_students(self) -> List[Dict[str, Any]]:
        """Obtiene todos los estudiantes activos"""
        return self.student_repo.get_active_students()
    
    def get_student_academic_metrics(
        self, 
        student_id: int, 
        academic_year: int, 
        trimester: Optional[int] = None
    ) -> Optional[AcademicMetrics]:
        """Obtiene métricas académicas de un estudiante"""
        
        # Obtener calificaciones del estudiante
        scores = self.score_repo.get_by_student(student_id, academic_year)
        
        if not scores:
            return None
        
        # Calcular métricas usando el engine
        return self.engine.calculate_academic_metrics(student_id, scores, academic_year, trimester)
    
    def get_student_financial_metrics(self, student_id: int) -> FinancialMetrics:
        """Obtiene métricas financieras de un estudiante"""
        
        # Obtener pagos del estudiante
        payments = self.payment_repo.get_by_student(student_id)
        
        # Calcular métricas usando el engine
        return self.engine.calculate_financial_metrics(student_id, payments)
    
    def get_student_complete_profile(self, student_id: int, academic_year: int) -> Dict[str, Any]:
        """Obtiene perfil completo del estudiante"""
        
        # Información básica
        student = self.get_student(student_id)
        if not student:
            return {}
        
        # Métricas académicas
        academic_metrics = self.get_student_academic_metrics(student_id, academic_year)
        
        # Métricas financieras
        financial_metrics = self.get_student_financial_metrics(student_id)
        
        # Alertas
        alerts = []
        if academic_metrics:
            alerts.extend(self.engine.detect_academic_alerts(academic_metrics))
        alerts.extend(self.engine.detect_financial_alerts(financial_metrics))
        
        return {
            'student_info': student,
            'academic_metrics': academic_metrics,
            'financial_metrics': financial_metrics,
            'alerts': alerts,
            'risk_level': self._calculate_risk_level(alerts)
        }
    
    def get_students_at_risk(self, academic_year: int) -> List[Dict[str, Any]]:
        """Identifica estudiantes en riesgo académico o financiero"""
        
        at_risk_students = []
        active_students = self.get_active_students()
        
        for student in active_students:
            profile = self.get_student_complete_profile(student['id'], academic_year)
            
            if profile['risk_level'] in ['medium', 'high']:
                at_risk_students.append(profile)
        
        return at_risk_students
    
    def transfer_student(self, student_id: int, new_classroom_id: int) -> bool:
        """Transfiere un estudiante a otra aula"""
        
        # Validar que exista el estudiante y el aula
        student = self.student_repo.get_by_id(student_id)
        new_classroom = self.classroom_repo.get_by_id(new_classroom_id)
        
        if not student or not new_classroom:
            return False
        
        # Actualizar aula
        return self.update_student(student_id, {'classroom_id': new_classroom_id})
    
    def get_classroom_summary(self, classroom_id: int, academic_year: int) -> Dict[str, Any]:
        """Obtiene resumen de un aula"""
        
        # Estudiantes del aula
        students = self.get_students_by_classroom(classroom_id)
        
        if not students:
            return {}
        
        # Calcular métricas del aula
        students_scores = {}
        for student in students:
            scores = self.student_repo.scores.get_by_student(student['id'], academic_year)
            students_scores[student['id']] = scores
        
        classroom_performance = self.engine.calculate_classroom_performance(
            students_scores, academic_year
        )
        
        # Información del aula
        classroom_info = self.classroom_repo.get_with_details()
        classroom_data = next(
            (c for c in classroom_info if c['id'] == classroom_id), 
            {}
        )
        
        return {
            'classroom_info': classroom_data,
            'student_count': len(students),
            'performance': classroom_performance,
            'students': students
        }
    
    def _calculate_risk_level(self, alerts: List[Alert]) -> str:
        """Calcula nivel de riesgo basado en alertas"""
        
        if not alerts:
            return 'low'
        
        high_severity_count = len([a for a in alerts if a.severity == 'high'])
        medium_severity_count = len([a for a in alerts if a.severity == 'medium'])
        
        if high_severity_count > 0:
            return 'high'
        elif medium_severity_count > 1:
            return 'medium'
        else:
            return 'low'
    
    def generate_student_report(self, student_id: int, academic_year: int) -> Dict[str, Any]:
        """Genera reporte completo para un estudiante"""
        
        profile = self.get_student_complete_profile(student_id, academic_year)
        
        if not profile:
            return {}
        
        # Información adicional
        student_info = profile['student_info']
        
        # Historial de pagos
        payments = self.payment_repo.get_by_student(student_id)
        
        # Calificaciones detalladas
        scores = self.student_repo.scores.get_by_student(student_id, academic_year)
        
        return {
            'basic_info': student_info,
            'academic_summary': profile['academic_metrics'],
            'financial_summary': profile['financial_metrics'],
            'alerts': profile['alerts'],
            'risk_level': profile['risk_level'],
            'payment_history': payments,
            'detailed_scores': scores,
            'generated_at': datetime.now().isoformat()
        }


# Instancia global del servicio
student_service = StudentService()
