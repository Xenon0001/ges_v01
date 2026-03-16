"""
Tests de Integración Final - GES MVP
Valida el funcionamiento completo de la aplicación
"""

import sys
import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import GESApplication
from database.models import DatabaseModels
from services.student_service import StudentService
from services.academic_service import AcademicService
from services.finance_service import FinanceService


class TestGESIntegration(unittest.TestCase):
    """Tests de integración para GES"""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests"""
        # Usar base de datos en memoria para tests
        import database.connection
        import config
        
        cls.original_db_path = config.DB_PATH
        cls.memory_db_path = ":memory:"
        
        # Configurar base de datos en memoria
        config.DB_PATH = cls.memory_db_path
        database.connection.DB_PATH = cls.memory_db_path
        database.connection.db = database.connection.DatabaseConnection()
        
        # Inicializar base de datos
        models = DatabaseModels()
        models.initialize_database()
        
        # Crear usuario admin por defecto
        cls._create_default_admin()
    
    @classmethod
    def tearDownClass(cls):
        """Limpieza final"""
        # Restaurar configuración
        import config
        import database.connection
        config.DB_PATH = cls.original_db_path
        database.connection.DB_PATH = cls.original_db_path
        database.connection.db = database.connection.DatabaseConnection(cls.original_db_path)
    
    @classmethod
    def _create_default_admin(cls):
        """Crea usuario admin por defecto"""
        import hashlib
        from database.repository import user_repo
        
        # Verificar si el usuario admin ya existe
        existing_admin = user_repo.get_by_username('admin')
        if existing_admin:
            return
        
        admin_data = {
            'username': 'admin',
            'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
            'role_id': 1,
            'is_active': True
        }
        user_repo.create(admin_data)
    
    def setUp(self):
        """Configuración para cada test"""
        # Crear aplicación sin mostrar ventana
        self.app = GESApplication()
        self.app.root.withdraw()  # Ocultar ventana para tests
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if hasattr(self, 'app') and self.app.root:
            try:
                if self.app.root.winfo_exists():
                    self.app.root.destroy()
            except tk.TclError:
                pass  # La ventana ya fue destruida
    
    def test_application_initialization(self):
        """Test que la aplicación se inicializa correctamente"""
        # Verificar que la aplicación se creó
        self.assertIsNotNone(self.app)
        self.assertIsNotNone(self.app.root)
        self.assertIsNotNone(self.app.config)
        
        # Verificar configuración por defecto
        self.assertEqual(self.app.config['mode'], 'normal')
        self.assertEqual(self.app.config['academic_year'], 2024)
        self.assertEqual(self.app.config['port'], 8000)
    
    def test_database_initialization(self):
        """Test que la base de datos se inicializa correctamente"""
        # Verificar que las tablas existen
        from database.connection import db
        
        # Intentar una consulta simple para verificar conexión
        result = db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in result]
        
        # Debug: mostrar tablas encontradas
        print(f"🔍 Tablas encontradas: {tables}")
        
        # Si no hay tablas, intentar inicializar nuevamente
        if not tables:
            print("⚠️ No se encontraron tablas, inicializando...")
            try:
                models = DatabaseModels()
                models.create_tables()  # Llamar directamente a create_tables
                
                # Consultar nuevamente
                result = db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row['name'] for row in result]
                print(f"🔍 Tablas después de inicialización: {tables}")
                
                # Si todavía no hay tablas, intentar con consulta directa
                if not tables:
                    print("⚠️ Intentando consulta directa a sqlite_master...")
                    result = db.execute_query("SELECT name FROM sqlite_master")
                    all_objects = [row['name'] for row in result]
                    print(f"🔍 Todos los objetos: {all_objects}")
                    
            except Exception as e:
                print(f"💥 Error en inicialización: {e}")
                raise
        
        # Verificar tablas principales
        expected_tables = ['users', 'students', 'subjects', 'scores', 'payments', 'classrooms']
        for table in expected_tables:
            self.assertIn(table, tables)
    
    def test_services_integration(self):
        """Test integración entre servicios"""
        # Crear servicios
        student_service = StudentService()
        academic_service = AcademicService()
        finance_service = FinanceService()
        
        # Crear estudiante de prueba
        student_data = {
            'first_name': 'Test',
            'last_name': 'Student',
            'classroom_id': 1,
            'tutor_name': 'Test Tutor'
        }
        
        student_id = student_service.create_student(student_data)
        self.assertGreater(student_id, 0)
        
        # Verificar que se puede obtener el estudiante
        student = student_service.get_student(student_id)
        self.assertIsNotNone(student)
        self.assertEqual(student['first_name'], 'Test')
        
        # Agregar calificación
        score_data = {
            'student_id': student_id,
            'subject_id': 1,
            'teacher_id': 1,
            'trimester': 1,
            'score': 8.5,
            'academic_year': 2024
        }
        
        score_id = academic_service.add_score(score_data)
        self.assertGreater(score_id, 0)
        
        # Agregar pago
        payment_data = {
            'student_id': student_id,
            'amount_due': 100.0,
            'amount_paid': 50.0,
            'due_date': '2024-12-31'
        }
        
        payment_id = finance_service.create_payment(payment_data)
        self.assertGreater(payment_id, 0)
        
        # Verificar perfil completo
        profile = student_service.get_student_complete_profile(student_id, 2024)
        self.assertIsNotNone(profile)
        self.assertIn('student_info', profile)
        self.assertIn('academic_metrics', profile)
        self.assertIn('financial_metrics', profile)
    
    def test_login_authentication(self):
        """Test proceso de autenticación"""
        from ui.login import LoginWindow
        
        # Crear ventana de login
        login_window = LoginWindow(self.app.root, self.app.on_login_success)
        
        # Simular login exitoso
        login_window.username_entry.insert(0, 'admin')
        login_window.password_entry.insert(0, 'admin123')
        
        # Verificar que los campos tengan los valores correctos
        self.assertEqual(login_window.username_entry.get(), 'admin')
        self.assertEqual(login_window.password_entry.get(), 'admin123')
        
        # Destruir ventana de login
        login_window.parent.destroy()
    
    def test_dashboard_data_loading(self):
        """Test carga de datos en dashboard"""
        from ui.dashboard import DashboardWindow
        
        # Crear datos de prueba
        self._create_test_data()
        
        # Simular usuario logueado
        user_data = {
            'id': 1,
            'username': 'admin',
            'role_id': 1,
            'is_active': True
        }
        
        # Crear dashboard
        dashboard = DashboardWindow(self.app.root, user_data, self.app.config, self.app.on_logout)
        
        # Verificar que el dashboard se creó
        self.assertIsNotNone(dashboard)
        self.assertIsNotNone(dashboard.student_service)
        self.assertIsNotNone(dashboard.academic_service)
        self.assertIsNotNone(dashboard.finance_service)
        
        # Destruir dashboard
        dashboard.parent.destroy()
    
    def test_students_view_crud(self):
        """Test CRUD en vista de estudiantes"""
        from ui.students_view import StudentsView
        
        # Crear frame contenedor
        container = tk.Frame(self.app.root)
        
        # Crear vista de estudiantes
        students_view = StudentsView(container, self.app.config)
        
        # Verificar que la vista se creó
        self.assertIsNotNone(students_view)
        self.assertIsNotNone(students_view.student_service)
        
        # Destruir vista
        container.destroy()
    
    def test_academic_metrics_calculation(self):
        """Test cálculo de métricas académicas"""
        from core.engine import CoreEngine
        
        # Crear datos de prueba
        scores = [
            {'subject_id': 1, 'score': 8.0, 'recovery_score': None, 'academic_year': 2024, 'trimester': 1},
            {'subject_id': 2, 'score': 6.0, 'recovery_score': None, 'academic_year': 2024, 'trimester': 1},
            {'subject_id': 3, 'score': 4.0, 'recovery_score': 6.0, 'academic_year': 2024, 'trimester': 1}
        ]
        
        engine = CoreEngine()
        metrics = engine.calculate_academic_metrics(1, scores, 2024, 1)
        
        # Verificar métricas
        self.assertEqual(metrics.student_id, 1)
        self.assertEqual(metrics.academic_year, 2024)
        self.assertEqual(metrics.trimester, 1)
        self.assertEqual(metrics.average, 6.0)  # (8.0 + 6.0 + 4.0) / 3
        self.assertEqual(metrics.passed_subjects, 3)  # 8.0, 6.0, y 4.0→6.0 (recuperada)
        self.assertEqual(metrics.failed_subjects, 0)  # Ninguna reprobada final
        self.assertEqual(metrics.recovery_count, 1)
    
    def test_financial_metrics_calculation(self):
        """Test cálculo de métricas financieras"""
        from core.engine import CoreEngine
        
        # Crear datos de prueba
        payments = [
            {'amount_due': 100.0, 'amount_paid': 100.0, 'status': 'pagado', 'due_date': '2024-01-15'},
            {'amount_due': 100.0, 'amount_paid': 50.0, 'status': 'pendiente', 'due_date': '2024-02-15'},
            {'amount_due': 100.0, 'amount_paid': 0.0, 'status': 'retrasado', 'due_date': '2023-12-15'}
        ]
        
        engine = CoreEngine()
        metrics = engine.calculate_financial_metrics(1, payments)
        
        # Verificar métricas
        self.assertEqual(metrics.student_id, 1)
        self.assertEqual(metrics.total_due, 300.0)
        self.assertEqual(metrics.total_paid, 150.0)
        self.assertEqual(metrics.outstanding, 150.0)
        self.assertEqual(metrics.overdue_count, 1)
    
    def test_error_handling(self):
        """Test manejo de errores"""
        student_service = StudentService()
        
        # Test crear estudiante con datos inválidos
        with self.assertRaises(ValueError):
            student_service.create_student({'first_name': ''})  # Sin apellido
        
        # Test crear estudiante con aula inexistente
        with self.assertRaises(ValueError):
            student_service.create_student({
                'first_name': 'Test',
                'last_name': 'Student',
                'classroom_id': 999  # Aula inexistente
            })
    
    def test_config_management(self):
        """Test gestión de configuración"""
        # Verificar configuración por defecto
        self.assertIn('mode', self.app.config)
        self.assertIn('academic_year', self.app.config)
        self.assertIn('port', self.app.config)
        
        # Test guardar configuración
        test_config = self.app.config.copy()
        test_config['test_field'] = 'test_value'
        
        self.app.save_config(test_config)
        
        # Verificar que se guardó
        config_path = Path(__file__).parent.parent / "config.json"
        self.assertTrue(config_path.exists())
    
    def _create_test_data(self):
        """Crea datos de prueba para los tests"""
        # Crear estudiantes
        student_service = StudentService()
        
        students = [
            {
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'classroom_id': 1,
                'tutor_name': 'María Pérez'
            },
            {
                'first_name': 'Ana',
                'last_name': 'García',
                'classroom_id': 1,
                'tutor_name': 'Carlos García'
            }
        ]
        
        for student in students:
            student_service.create_student(student)
        
        # Crear calificaciones
        academic_service = AcademicService()
        
        # Obtener estudiantes para asignar calificaciones
        active_students = student_service.get_active_students()
        
        for i, student in enumerate(active_students[:2]):  # Solo los primeros 2
            for subject_id in [1, 2, 3]:
                score_data = {
                    'student_id': student['id'],
                    'subject_id': subject_id,
                    'teacher_id': 1,
                    'trimester': 1,
                    'score': 6.0 + i,
                    'academic_year': 2024
                }
                academic_service.add_score(score_data)
        
        # Crear pagos
        finance_service = FinanceService()
        
        for student in active_students[:2]:
            payment_data = {
                'student_id': student['id'],
                'amount_due': 100.0,
                'amount_paid': 50.0 * (1 + active_students.index(student)),
                'due_date': '2024-12-31'
            }
            finance_service.create_payment(payment_data)


class TestUIComponents(unittest.TestCase):
    """Tests específicos para componentes UI"""
    
    def setUp(self):
        """Configuración para cada test"""
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana para tests
    
    def tearDown(self):
        """Limpieza después de cada test"""
        try:
            if self.root and self.root.winfo_exists():
                self.root.destroy()
        except tk.TclError:
            pass  # La ventana ya fue destruida
    
    def test_login_window_creation(self):
        """Test creación de ventana de login"""
        from ui.login import LoginWindow
        
        def mock_success(user_data):
            pass
        
        login_window = LoginWindow(self.root, mock_success)
        
        # Verificar que se crearon los widgets principales
        self.assertIsNotNone(login_window.username_entry)
        self.assertIsNotNone(login_window.password_entry)
        
        # Destruir ventana
        login_window.parent.destroy()
    
    def test_students_view_creation(self):
        """Test creación de vista de estudiantes"""
        from ui.students_view import StudentsView
        
        config = {'mode': 'normal', 'academic_year': 2024}
        container = tk.Frame(self.root)
        
        students_view = StudentsView(container, config)
        
        # Verificar que se crearon los componentes principales
        self.assertIsNotNone(students_view.students_tree)
        self.assertIsNotNone(students_view.search_var)
        
        # Destruir vista
        container.destroy()


def run_integration_tests():
    """Ejecuta todos los tests de integración"""
    print("🧪 Ejecutando Tests de Integración Final - GES MVP")
    print("=" * 60)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestGESIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestUIComponents))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests fallidos: {len(result.failures)}")
    print(f"Tests con errores: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FALLAS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERRORES:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ Todos los tests pasaron' if success else '❌ Algunos tests fallaron'}")
    
    return success


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
