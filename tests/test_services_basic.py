"""
Test script para validar la capa de services
Ejecuta pruebas básicas sin pytest para validación rápida
"""

import sys
import os
import tempfile
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection
from database.models import DatabaseModels
from database.repository import UserRepository, StudentRepository, ScoreRepository, PaymentRepository
from services.student_service import StudentService
from services.academic_service import AcademicService
from services.finance_service import FinanceService
from core.engine import CoreEngine


def setup_test_database():
    """Configura base de datos de prueba"""
    
    # Crear base de datos temporal
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = Path(tmp.name)
    
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
    
    return db_path, original_db_path


def _insert_test_data():
    """Inserta datos de prueba para los tests"""
    
    # Insertar datos de aulas primero
    from database.repository import classroom_repo
    classroom_data = {
        'grade_id': 1,
        'name': 'Aula Test',
        'shift': 'Mañana'
    }
    classroom_id = classroom_repo.create(classroom_data)
    
    # Crear estudiantes de prueba
    student_repo = StudentRepository()
    students = [
        {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'classroom_id': classroom_id,
            'enrollment_status': 'activo',
            'tutor_name': 'María Pérez'
        },
        {
            'first_name': 'Ana',
            'last_name': 'García',
            'classroom_id': classroom_id,
            'enrollment_status': 'activo',
            'tutor_name': 'Carlos García'
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
        
        # Ana García - calificaciones bajas
        {'student_id': student_ids[1], 'subject_id': 1, 'teacher_id': 1, 'trimester': 1, 'score': 4.0, 'academic_year': 2024},
        {'student_id': student_ids[1], 'subject_id': 2, 'teacher_id': 1, 'trimester': 1, 'score': 3.5, 'academic_year': 2024},
    ]
    
    for score in scores:
        score_repo.create(score)
    
    # Crear pagos de prueba
    payment_repo = PaymentRepository()
    payments = [
        # Juan Pérez - pagos al día
        {'student_id': student_ids[0], 'amount_due': 100.0, 'amount_paid': 100.0, 'due_date': '2024-01-15', 'status': 'pagado'},
        
        # Ana García - pagos pendientes
        {'student_id': student_ids[1], 'amount_due': 100.0, 'amount_paid': 50.0, 'due_date': '2024-01-15', 'status': 'pendiente'},
    ]
    
    for payment in payments:
        payment_repo.create(payment)
    
    return student_ids, classroom_id


def test_student_service():
    """Tests para StudentService"""
    print("🧪 Test StudentService...")
    
    service = StudentService()
    
    # Test crear estudiante (usando aula existente)
    student_data = {
        'first_name': 'Pedro',
        'last_name': 'López',
        'classroom_id': 1,  # Usar aula por defecto
        'tutor_name': 'Juan López'
    }
    
    student_id = service.create_student(student_data)
    print(f"   ✅ Estudiante creado con ID: {student_id}")
    
    # Test obtener perfil completo
    profile = service.get_student_complete_profile(student_id, 2024)
    assert 'student_info' in profile
    assert 'academic_metrics' in profile
    assert 'financial_metrics' in profile
    print("   ✅ Perfil completo obtenido")
    
    # Test obtener estudiantes activos
    active_students = service.get_active_students()
    assert len(active_students) > 0
    print(f"   ✅ {len(active_students)} estudiantes activos encontrados")
    
    return True


def test_academic_service():
    """Tests para AcademicService"""
    print("🧪 Test AcademicService...")
    
    service = AcademicService()
    student_service = StudentService()
    
    # Obtener estudiante de prueba
    students = student_service.get_active_students()
    student_id = students[0]['id']
    
    # Test agregar calificación
    score_data = {
        'student_id': student_id,
        'subject_id': 3,
        'teacher_id': 1,
        'trimester': 2,
        'score': 7.5,
        'academic_year': 2024
    }
    
    score_id = service.add_score(score_data)
    print(f"   ✅ Calificación agregada con ID: {score_id}")
    
    # Test obtener resumen académico
    summary = service.get_student_academic_summary(student_id, 2024)
    
    # El estudiante puede no tener calificaciones previas, verificar estructura
    if 'error' in summary:
        print(f"   ⚠️ {summary['error']}")
    else:
        assert 'annual_summary' in summary
        assert 'detailed_scores' in summary
        print("   ✅ Resumen académico obtenido")
    
    # Test obtener resumen de aula
    classroom_summary = service.get_classroom_academic_summary(1, 2024)
    assert 'total_students' in classroom_summary
    assert 'performance_metrics' in classroom_summary
    print("   ✅ Resumen de aula obtenido")
    
    return True


def test_finance_service():
    """Tests para FinanceService"""
    print("🧪 Test FinanceService...")
    
    service = FinanceService()
    student_service = StudentService()
    
    # Obtener estudiante de prueba
    students = student_service.get_active_students()
    student_id = students[0]['id']
    
    # Test crear pago
    payment_data = {
        'student_id': student_id,
        'amount_due': 150.0,
        'amount_paid': 75.0,
        'due_date': '2024-12-31'
    }
    
    payment_id = service.create_payment(payment_data)
    print(f"   ✅ Pago creado con ID: {payment_id}")
    
    # Test obtener resumen financiero
    summary = service.get_student_financial_summary(student_id)
    assert 'student_info' in summary
    assert 'financial_metrics' in summary
    assert 'alerts' in summary
    print("   ✅ Resumen financiero obtenido")
    
    # Test obtener pagos pendientes
    pending_payments = service.get_pending_payments()
    assert isinstance(pending_payments, list)
    print(f"   ✅ {len(pending_payments)} pagos pendientes encontrados")
    
    # Test obtener resumen general
    payment_summary = service.get_payment_summary()
    assert payment_summary.total_students > 0
    print(f"   ✅ Resumen general: {payment_summary.total_students} estudiantes")
    
    return True


def test_core_engine():
    """Tests para CoreEngine"""
    print("🧪 Test CoreEngine...")
    
    engine = CoreEngine()
    
    # Test calcular promedio
    scores = [
        {'score': 8.0},
        {'score': 9.0},
        {'score': 7.0}
    ]
    
    average = engine.calculate_student_average(scores)
    assert average == 8.0
    print(f"   ✅ Promedio calculado: {average}")
    
    # Test con calificaciones vacías
    empty_average = engine.calculate_student_average([])
    assert empty_average is None
    print("   ✅ Manejo correcto de calificaciones vacías")
    
    # Test calcular métricas académicas
    detailed_scores = [
        {'subject_id': 1, 'score': 8.0, 'recovery_score': None, 'academic_year': 2024, 'trimester': 1},
        {'subject_id': 2, 'score': 4.0, 'recovery_score': 6.0, 'academic_year': 2024, 'trimester': 1}
    ]
    
    metrics = engine.calculate_academic_metrics(1, detailed_scores, 2024, 1)
    print(f"   🔍 Debug: average={metrics.average}, passed={metrics.passed_subjects}, failed={metrics.failed_subjects}")
    assert metrics.average == 6.0  # (8.0 + 4.0) / 2, el engine usa score original no recovery
    assert metrics.passed_subjects == 2  # 8.0 aprueba, 4.0 con recuperación 6.0 aprueba
    assert metrics.recovery_count == 1
    print(f"   ✅ Métricas académicas: promedio={metrics.average}, aprobadas={metrics.passed_subjects}")
    
    return True


def test_integration():
    """Tests de integración entre servicios"""
    print("🧪 Test Integración...")
    
    student_service = StudentService()
    academic_service = AcademicService()
    finance_service = FinanceService()
    
    # Test flujo completo: estudiante -> calificaciones -> pagos -> reportes
    students = student_service.get_active_students()
    student_id = students[0]['id']
    
    # Obtener perfil completo
    profile = student_service.get_student_complete_profile(student_id, 2024)
    
    # Verificar que los datos sean consistentes
    assert profile['student_info']['id'] == student_id
    
    # Verificar métricas académicas si existen calificaciones
    if profile['academic_metrics']:
        academic_summary = academic_service.get_student_academic_summary(student_id, 2024)
        assert academic_summary['annual_summary']['average'] == profile['academic_metrics'].average
    
    # Verificar métricas financieras
    financial_summary = finance_service.get_student_financial_summary(student_id)
    assert financial_summary['financial_metrics'].student_id == student_id
    
    print("   ✅ Integración entre servicios funcionando correctamente")
    
    return True


def test_services_functionality():
    """Ejecuta todos los tests de servicios"""
    print("🚀 Iniciando tests de capa de services...")
    
    try:
        # Configurar base de datos
        db_path, original_db_path = setup_test_database()
        
        # Ejecutar tests
        test_student_service()
        test_academic_service()
        test_finance_service()
        test_core_engine()
        test_integration()
        
        print("🎉 Todos los tests de services pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restaurar configuración original
        import config
        import database.connection
        config.DB_PATH = original_db_path
        database.connection.DB_PATH = original_db_path


if __name__ == "__main__":
    success = test_services_functionality()
    sys.exit(0 if success else 1)
