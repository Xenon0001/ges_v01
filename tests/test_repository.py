"""
Tests para database/repository
Valida las operaciones CRUD de la capa de base de datos
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from database.connection import DatabaseConnection
from database.models import DatabaseModels
from database.repository import (
    UserRepository, StudentRepository, ScoreRepository,
    PaymentRepository, SubjectRepository, ClassroomRepository
)


@pytest.fixture
def temp_db():
    """Fixture para base de datos temporal"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = Path(tmp.name)
    
    # Usar base de datos temporal
    with patch('database.connection.DB_PATH', db_path):
        with patch('config.DB_PATH', db_path):
            connection = DatabaseConnection(db_path)
            
            # Inicializar tablas
            models = DatabaseModels()
            models.create_tables()
            models.insert_initial_data()
            
            yield connection
    
    # Limpiar
    if db_path.exists():
        os.unlink(db_path)


@pytest.fixture
def sample_user_data():
    """Datos de prueba para usuario"""
    return {
        'username': 'test_user',
        'password_hash': 'hashed_password',
        'role_id': 1,
        'is_active': True
    }


@pytest.fixture
def sample_student_data():
    """Datos de prueba para estudiante"""
    return {
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'classroom_id': 1,
        'enrollment_status': 'activo',
        'tutor_name': 'María Pérez'
    }


class TestBaseRepository:
    """Tests para el repository base"""
    
    def test_create_and_get_by_id(self, temp_db, sample_user_data):
        """Test crear y obtener por ID"""
        repo = UserRepository()
        
        # Crear
        user_id = repo.create(sample_user_data)
        assert user_id > 0
        
        # Obtener
        user = repo.get_by_id(user_id)
        assert user is not None
        assert user['username'] == sample_user_data['username']
        assert user['role_id'] == sample_user_data['role_id']
    
    def test_get_all(self, temp_db, sample_user_data):
        """Test obtener todos los registros"""
        repo = UserRepository()
        
        # Crear múltiples usuarios
        for i in range(3):
            data = sample_user_data.copy()
            data['username'] = f'user_{i}'
            repo.create(data)
        
        # Obtener todos
        users = repo.get_all()
        assert len(users) >= 3
    
    def test_update(self, temp_db, sample_user_data):
        """Test actualizar registro"""
        repo = UserRepository()
        
        # Crear
        user_id = repo.create(sample_user_data)
        
        # Actualizar
        update_data = {'is_active': False}
        rows_affected = repo.update(user_id, update_data)
        assert rows_affected == 1
        
        # Verificar
        updated_user = repo.get_by_id(user_id)
        assert updated_user['is_active'] == 0
    
    def test_delete(self, temp_db, sample_user_data):
        """Test eliminar registro"""
        repo = UserRepository()
        
        # Crear
        user_id = repo.create(sample_user_data)
        
        # Eliminar
        rows_affected = repo.delete(user_id)
        assert rows_affected == 1
        
        # Verificar
        deleted_user = repo.get_by_id(user_id)
        assert deleted_user is None


class TestUserRepository:
    """Tests específicos para UserRepository"""
    
    def test_get_by_username(self, temp_db, sample_user_data):
        """Test obtener usuario por username"""
        repo = UserRepository()
        
        # Crear
        repo.create(sample_user_data)
        
        # Buscar por username
        user = repo.get_by_username(sample_user_data['username'])
        assert user is not None
        assert user['username'] == sample_user_data['username']
    
    def test_get_active_users(self, temp_db, sample_user_data):
        """Test obtener usuarios activos"""
        repo = UserRepository()
        
        # Crear usuarios activos e inactivos
        active_data = sample_user_data.copy()
        active_data['username'] = 'active_user'
        repo.create(active_data)
        
        inactive_data = sample_user_data.copy()
        inactive_data['username'] = 'inactive_user'
        inactive_data['is_active'] = False
        repo.create(inactive_data)
        
        # Obtener activos
        active_users = repo.get_active_users()
        usernames = [u['username'] for u in active_users]
        assert 'active_user' in usernames
        assert 'inactive_user' not in usernames


class TestStudentRepository:
    """Tests específicos para StudentRepository"""
    
    def test_create_and_search_student(self, temp_db, sample_student_data):
        """Test crear y buscar estudiante"""
        repo = StudentRepository()
        
        # Crear
        student_id = repo.create(sample_student_data)
        assert student_id > 0
        
        # Buscar por nombre
        results = repo.search_by_name('Juan')
        assert len(results) > 0
        assert results[0]['first_name'] == 'Juan'
    
    def test_get_active_students(self, temp_db, sample_student_data):
        """Test obtener estudiantes activos"""
        repo = StudentRepository()
        
        # Crear estudiante activo
        repo.create(sample_student_data)
        
        # Crear estudiante inactivo
        inactive_data = sample_student_data.copy()
        inactive_data['first_name'] = 'María'
        inactive_data['enrollment_status'] = 'retirado'
        repo.create(inactive_data)
        
        # Obtener activos
        active_students = repo.get_active_students()
        names = [s['first_name'] for s in active_students]
        assert 'Juan' in names
        assert 'María' not in names


class TestScoreRepository:
    """Tests específicos para ScoreRepository"""
    
    def test_create_and_get_student_scores(self, temp_db):
        """Test crear y obtener calificaciones"""
        repo = ScoreRepository()
        
        # Crear calificación
        score_data = {
            'student_id': 1,
            'subject_id': 1,
            'teacher_id': 1,
            'trimester': 1,
            'score': 8.5,
            'academic_year': 2024
        }
        
        score_id = repo.create(score_data)
        assert score_id > 0
        
        # Obtener calificaciones del estudiante
        scores = repo.get_by_student(1, 2024)
        assert len(scores) > 0
        assert scores[0]['score'] == 8.5
    
    def test_calculate_average(self, temp_db):
        """Test calcular promedio de estudiante"""
        repo = ScoreRepository()
        
        # Crear múltiples calificaciones
        scores = [
            {'student_id': 1, 'subject_id': 1, 'teacher_id': 1, 'trimester': 1, 'score': 8.0, 'academic_year': 2024},
            {'student_id': 1, 'subject_id': 2, 'teacher_id': 1, 'trimester': 1, 'score': 9.0, 'academic_year': 2024},
            {'student_id': 1, 'subject_id': 3, 'teacher_id': 1, 'trimester': 1, 'score': 7.0, 'academic_year': 2024}
        ]
        
        for score in scores:
            repo.create(score)
        
        # Calcular promedio
        average = repo.get_student_average(1, 2024, 1)
        assert average == 8.0  # (8.0 + 9.0 + 7.0) / 3


class TestPaymentRepository:
    """Tests específicos para PaymentRepository"""
    
    def test_create_and_get_student_payments(self, temp_db):
        """Test crear y obtener pagos"""
        repo = PaymentRepository()
        
        # Crear pago
        payment_data = {
            'student_id': 1,
            'amount_due': 100.0,
            'amount_paid': 50.0,
            'due_date': '2024-12-31',
            'status': 'pendiente'
        }
        
        payment_id = repo.create(payment_data)
        assert payment_id > 0
        
        # Obtener pagos del estudiante
        payments = repo.get_by_student(1)
        assert len(payments) > 0
        assert payments[0]['amount_due'] == 100.0
    
    def test_debt_summary(self, temp_db):
        """Test resumen de deuda"""
        repo = PaymentRepository()
        
        # Crear múltiples pagos
        payments = [
            {'student_id': 1, 'amount_due': 100.0, 'amount_paid': 100.0, 'status': 'pagado'},
            {'student_id': 1, 'amount_due': 50.0, 'amount_paid': 25.0, 'status': 'pendiente'},
            {'student_id': 1, 'amount_due': 75.0, 'amount_paid': 0.0, 'status': 'pendiente'}
        ]
        
        for payment in payments:
            repo.create(payment)
        
        # Obtener resumen
        summary = repo.get_debt_summary(1)
        assert summary['total_due'] == 225.0
        assert summary['total_paid'] == 125.0
        assert summary['outstanding'] == 100.0


class TestSubjectRepository:
    """Tests específicos para SubjectRepository"""
    
    def test_get_subjects(self, temp_db):
        """Test obtener materias"""
        repo = SubjectRepository()
        
        # Obtener todas las materias (deben existir las iniciales)
        subjects = repo.get_all()
        assert len(subjects) > 0
        
        # Verificar que existen materias básicas
        subject_names = [s['name'] for s in subjects]
        assert 'Matemáticas' in subject_names
        assert 'Lenguaje' in subject_names


class TestClassroomRepository:
    """Tests específicos para ClassroomRepository"""
    
    def test_get_classrooms(self, temp_db):
        """Test obtener aulas"""
        repo = ClassroomRepository()
        
        # Las aulas se crean con datos iniciales
        # Este test verifica que la estructura funciona
        classrooms = repo.get_all()
        assert isinstance(classrooms, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
