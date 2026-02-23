"""
Tests para services layer
Valida la integración entre repositories y core engine
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, date

# Agregar el directorio raíz al path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection
from database.models import DatabaseModels
from database.repository import UserRepository, StudentRepository, ScoreRepository, PaymentRepository
from services.student_service import StudentService
from services.academic_service import AcademicService
from services.finance_service import FinanceService
from core.engine import CoreEngine, AcademicMetrics, FinancialMetrics, AlertType


@pytest.fixture
def temp_db():
    """Fixture para base de datos temporal con datos de prueba"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = Path(tmp.name)
    
    try:
        # Modificar el path de la base de datos
        import database.connection
        import config
        original_db_path = config.DB_PATH
        config.DB_PATH = db_path
        database.connection.DB_PATH = db_path
        
        # Forzar recreación de conexión
        database.connection.db = database.connection.DatabaseConnection(db_path)
        
        # Inicializar base de datos
        models = DatabaseModels()
        models.initialize_database()
        
        # Insertar datos de prueba
        _insert_test_data()
        
        yield db_path
        
    finally:
        # Restaurar path original
        config.DB_PATH = original_db_path
        database.connection.DB_PATH = original_db_path
        
        # Limpiar archivo temporal
        if db_path.exists():
            os.unlink(db_path)


def _insert_test_data():
    """Inserta datos de prueba para los tests"""
    
    # Crear usuario de prueba
    user_repo = UserRepository()
    user_data = {
        'username': 'test_director',
        'password_hash': 'hashed_password',
        'role_id': 1,
        'is_active': True
    }
    user_repo.create(user_data)
    
    # Crear estudiantes de prueba
    student_repo = StudentRepository()
    students = [
        {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'classroom_id': 1,
            'enrollment_status': 'activo',
            'tutor_name': 'María Pérez'
        },
        {
            'first_name': 'Ana',
            'last_name': 'García',
            'classroom_id': 1,
            'enrollment_status': 'activo',
            'tutor_name': 'Carlos García'
        },
        {
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'classroom_id': 2,
            'enrollment_status': 'activo',
            'tutor_name': 'Laura Martínez'
        }
    ]
    
    student_ids = []
    for student in students:
        student_id = student_repo.create(student)
        student_ids.append(student_id)
    
    # Crear calificaciones de prueba
    score_repo = ScoreRepository()
    scores = [
        # Juan Pérez - buenas calificaciones
        {'student_id': student_ids[0], 'subject_id': 1, 'teacher_id': 1, 'trimester': 1, 'score': 8.5, 'academic_year': 2024},
        {'student_id': student_ids[0], 'subject_id': 2, 'teacher_id': 1, 'trimester': 1, 'score': 9.0, 'academic_year': 2024},
        {'student_id': student_ids[0], 'subject_id': 3, 'teacher_id': 1, 'trimester': 1, 'score': 7.5, 'academic_year': 2024},
        
        # Ana García - calificaciones promedio
        {'student_id': student_ids[1], 'subject_id': 1, 'teacher_id': 1, 'trimester': 1, 'score': 6.0, 'academic_year': 2024},
        {'student_id': student_ids[1], 'subject_id': 2, 'teacher_id': 1, 'trimester': 1, 'score': 5.5, 'academic_year': 2024},
        {'student_id': student_ids[1], 'subject_id': 3, 'teacher_id': 1, 'trimester': 1, 'score': 4.0, 'academic_year': 2024},
        
        # Luis Martínez - bajas calificaciones
        {'student_id': student_ids[2], 'subject_id': 1, 'teacher_id': 1, 'trimester': 1, 'score': 3.5, 'academic_year': 2024},
        {'student_id': student_ids[2], 'subject_id': 2, 'teacher_id': 1, 'trimester': 1, 'score': 4.0, 'academic_year': 2024},
        {'student_id': student_ids[2], 'subject_id': 3, 'teacher_id': 1, 'trimester': 1, 'score': 3.0, 'academic_year': 2024},
    ]
    
    for score in scores:
        score_repo.create(score)
    
    # Crear pagos de prueba
    payment_repo = PaymentRepository()
    payments = [
        # Juan Pérez - pagos al día
        {'student_id': student_ids[0], 'amount_due': 100.0, 'amount_paid': 100.0, 'due_date': '2024-01-15', 'status': 'pagado'},
        {'student_id': student_ids[0], 'amount_due': 100.0, 'amount_paid': 100.0, 'due_date': '2024-02-15', 'status': 'pagado'},
        
        # Ana García - pagos pendientes
        {'student_id': student_ids[1], 'amount_due': 100.0, 'amount_paid': 50.0, 'due_date': '2024-01-15', 'status': 'pendiente'},
        {'student_id': student_ids[1], 'amount_due': 100.0, 'amount_paid': 0.0, 'due_date': '2024-02-15', 'status': 'pendiente'},
        
        # Luis Martínez - pagos vencidos
        {'student_id': student_ids[2], 'amount_due': 100.0, 'amount_paid': 0.0, 'due_date': '2023-12-15', 'status': 'retrasado'},
        {'student_id': student_ids[2], 'amount_due': 100.0, 'amount_paid': 25.0, 'due_date': '2024-01-15', 'status': 'retrasado'},
    ]
    
    for payment in payments:
        payment_repo.create(payment)


class TestStudentService:
    """Tests para StudentService"""
    
    def test_create_student(self, temp_db):
        """Test crear estudiante"""
        service = StudentService()
        
        student_data = {
            'first_name': 'Pedro',
            'last_name': 'López',
            'classroom_id': 1,
            'tutor_name': 'Juan López'
        }
        
        student_id = service.create_student(student_data)
        assert student_id > 0
        
        # Verificar que se creó
        student = service.get_student(student_id)
        assert student is not None
        assert student['first_name'] == 'Pedro'
        assert student['enrollment_status'] == 'activo'
    
    def test_create_student_invalid_data(self, temp_db):
        """Test crear estudiante con datos inválidos"""
        service = StudentService()
        
        # Sin nombre
        with pytest.raises(ValueError):
            service.create_student({'last_name': 'López'})
        
        # Aula inexistente
        with pytest.raises(ValueError):
            service.create_student({
                'first_name': 'Pedro',
                'last_name': 'López',
                'classroom_id': 999
            })
    
    def test_get_student_complete_profile(self, temp_db):
        """Test obtener perfil completo de estudiante"""
        service = StudentService()
        
        # Obtener primer estudiante de prueba
        students = service.get_active_students()
        assert len(students) > 0
        
        student_id = students[0]['id']
        profile = service.get_student_complete_profile(student_id, 2024)
        
        assert 'student_info' in profile
        assert 'academic_metrics' in profile
        assert 'financial_metrics' in profile
        assert 'alerts' in profile
        assert 'risk_level' in profile
        
        # Verificar métricas académicas
        if profile['academic_metrics']:
            assert profile['academic_metrics'].student_id == student_id
            assert profile['academic_metrics'].academic_year == 2024
    
    def test_get_students_at_risk(self, temp_db):
        """Test identificar estudiantes en riesgo"""
        service = StudentService()
        
        at_risk_students = service.get_students_at_risk(2024)
        
        # Debería encontrar estudiantes con bajas calificaciones o problemas financieros
        assert isinstance(at_risk_students, list)
        
        # Verificar estructura de datos
        for student in at_risk_students:
            assert 'student_info' in student
            assert 'risk_level' in student
            assert student['risk_level'] in ['medium', 'high']


class TestAcademicService:
    """Tests para AcademicService"""
    
    def test_add_score(self, temp_db):
        """Test agregar calificación"""
        service = AcademicService()
        
        # Obtener estudiante de prueba
        student_service = StudentService()
        students = student_service.get_active_students()
        student_id = students[0]['id']
        
        score_data = {
            'student_id': student_id,
            'subject_id': 1,
            'teacher_id': 1,
            'trimester': 2,
            'score': 8.0,
            'academic_year': 2024
        }
        
        score_id = service.add_score(score_data)
        assert score_id > 0
    
    def test_add_score_invalid_data(self, temp_db):
        """Test agregar calificación con datos inválidos"""
        service = AcademicService()
        
        # Calificación fuera de rango
        with pytest.raises(ValueError):
            service.add_score({
                'student_id': 1,
                'subject_id': 1,
                'teacher_id': 1,
                'trimester': 1,
                'score': 15.0,  # Máximo es 10
                'academic_year': 2024
            })
        
        # Trimestre inválido
        with pytest.raises(ValueError):
            service.add_score({
                'student_id': 1,
                'subject_id': 1,
                'teacher_id': 1,
                'trimester': 4,  # Solo 1, 2, 3
                'score': 8.0,
                'academic_year': 2024
            })
    
    def test_get_student_academic_summary(self, temp_db):
        """Test obtener resumen académico de estudiante"""
        service = AcademicService()
        
        # Obtener estudiante de prueba
        student_service = StudentService()
        students = student_service.get_active_students()
        student_id = students[0]['id']
        
        summary = service.get_student_academic_summary(student_id, 2024)
        
        assert 'annual_summary' in summary
        assert 'trimester_breakdown' in summary
        assert 'detailed_scores' in summary
        assert 'academic_alerts' in summary
        assert 'academic_status' in summary
        
        # Verificar que tenga calificaciones
        assert len(summary['detailed_scores']) > 0
    
    def test_get_classroom_academic_summary(self, temp_db):
        """Test obtener resumen académico de aula"""
        service = AcademicService()
        
        summary = service.get_classroom_academic_summary(1, 2024)
        
        assert 'total_students' in summary
        assert 'performance_metrics' in summary
        assert 'students_at_risk' in summary
        assert 'top_performers' in summary
        assert 'subject_performance' in summary
        
        # Debería tener estudiantes
        assert summary['total_students'] > 0


class TestFinanceService:
    """Tests para FinanceService"""
    
    def test_create_payment(self, temp_db):
        """Test crear pago"""
        service = FinanceService()
        
        # Obtener estudiante de prueba
        student_service = StudentService()
        students = student_service.get_active_students()
        student_id = students[0]['id']
        
        payment_data = {
            'student_id': student_id,
            'amount_due': 150.0,
            'amount_paid': 50.0,
            'due_date': '2024-12-31'
        }
        
        payment_id = service.create_payment(payment_data)
        assert payment_id > 0
    
    def test_create_payment_invalid_data(self, temp_db):
        """Test crear pago con datos inválidos"""
        service = FinanceService()
        
        # Monto negativo
        with pytest.raises(ValueError):
            service.create_payment({
                'student_id': 1,
                'amount_due': -100.0
            })
        
        # Estudiante inexistente
        with pytest.raises(ValueError):
            service.create_payment({
                'student_id': 999,
                'amount_due': 100.0
            })
    
    def test_record_payment(self, temp_db):
        """Test registrar pago parcial"""
        service = FinanceService()
        
        # Obtener pago pendiente de prueba
        pending_payments = service.get_pending_payments()
        if pending_payments:
            payment_id = pending_payments[0]['id']
            original_paid = pending_payments[0]['amount_paid']
            
            # Registrar pago adicional
            success = service.record_payment(payment_id, 25.0)
            assert success
            
            # Verificar que se actualizó
            updated_payment = service.payment_repo.get_by_id(payment_id)
            assert updated_payment['amount_paid'] == original_paid + 25.0
    
    def test_get_student_financial_summary(self, temp_db):
        """Test obtener resumen financiero de estudiante"""
        service = FinanceService()
        
        # Obtener estudiante de prueba
        student_service = StudentService()
        students = student_service.get_active_students()
        student_id = students[0]['id']
        
        summary = service.get_student_financial_summary(student_id)
        
        assert 'student_info' in summary
        assert 'financial_metrics' in summary
        assert 'alerts' in summary
        assert 'payment_details' in summary
        assert 'payment_status' in summary
        assert 'risk_level' in summary
        
        # Verificar métricas financieras
        metrics = summary['financial_metrics']
        assert isinstance(metrics, FinancialMetrics)
        assert metrics.student_id == student_id
    
    def test_get_financial_dashboard_data(self, temp_db):
        """Test obtener datos de dashboard financiero"""
        service = FinanceService()
        
        dashboard_data = service.get_financial_dashboard_data()
        
        assert 'summary' in dashboard_data
        assert 'overdue_payments' in dashboard_data
        assert 'tutor_groups' in dashboard_data
        assert 'students_at_risk' in dashboard_data
        assert 'critical_alerts' in dashboard_data
        assert 'generated_at' in dashboard_data
        
        # Verificar resumen
        summary = dashboard_data['summary']
        assert summary.total_students > 0


class TestCoreEngine:
    """Tests para CoreEngine"""
    
    def test_calculate_student_average(self, temp_db):
        """Test calcular promedio de estudiante"""
        engine = CoreEngine()
        
        scores = [
            {'score': 8.0},
            {'score': 9.0},
            {'score': 7.0}
        ]
        
        average = engine.calculate_student_average(scores)
        assert average == 8.0
    
    def test_calculate_student_average_empty(self, temp_db):
        """Test calcular promedio sin calificaciones"""
        engine = CoreEngine()
        
        average = engine.calculate_student_average([])
        assert average is None
    
    def test_calculate_academic_metrics(self, temp_db):
        """Test calcular métricas académicas"""
        engine = CoreEngine()
        
        scores = [
            {'subject_id': 1, 'score': 8.0, 'recovery_score': None, 'academic_year': 2024, 'trimester': 1},
            {'subject_id': 2, 'score': 4.0, 'recovery_score': 6.0, 'academic_year': 2024, 'trimester': 1},
            {'subject_id': 3, 'score': 3.0, 'recovery_score': None, 'academic_year': 2024, 'trimester': 1}
        ]
        
        metrics = engine.calculate_academic_metrics(1, scores, 2024, 1)
        
        assert isinstance(metrics, AcademicMetrics)
        assert metrics.student_id == 1
        assert metrics.academic_year == 2024
        assert metrics.trimester == 1
        assert metrics.average == 5.0  # (8.0 + 6.0 + 3.0) / 3
        assert metrics.passed_subjects == 2  # 8.0 y 6.0 (recuperación)
        assert metrics.failed_subjects == 1  # 3.0
        assert metrics.recovery_count == 1
    
    def test_detect_academic_alerts(self, temp_db):
        """Test detectar alertas académicas"""
        engine = CoreEngine()
        
        # Estudiante con promedio bajo
        metrics = AcademicMetrics(
            student_id=1,
            academic_year=2024,
            trimester=1,
            average=3.5,
            subject_count=3,
            passed_subjects=0,
            failed_subjects=3,
            recovery_count=0
        )
        
        alerts = engine.detect_academic_alerts(metrics)
        
        assert len(alerts) > 0
        assert any(alert.type == AlertType.RENDIMIENTO for alert in alerts)
        assert any(alert.severity == 'high' for alert in alerts)
    
    def test_calculate_financial_metrics(self, temp_db):
        """Test calcular métricas financieras"""
        engine = CoreEngine()
        
        payments = [
            {'amount_due': 100.0, 'amount_paid': 100.0, 'status': 'pagado', 'due_date': '2024-01-15'},
            {'amount_due': 100.0, 'amount_paid': 50.0, 'status': 'pendiente', 'due_date': '2024-02-15'},
            {'amount_due': 100.0, 'amount_paid': 0.0, 'status': 'retrasado', 'due_date': '2023-12-15'}
        ]
        
        metrics = engine.calculate_financial_metrics(1, payments)
        
        assert isinstance(metrics, FinancialMetrics)
        assert metrics.student_id == 1
        assert metrics.total_due == 300.0
        assert metrics.total_paid == 150.0
        assert metrics.outstanding == 150.0
        assert metrics.overdue_count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
