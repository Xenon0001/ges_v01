"""
Test script para validar la capa de base de datos
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
from database.repository import UserRepository, StudentRepository


def test_basic_functionality():
    """Test básico de funcionalidad de la base de datos"""
    print("🧪 Iniciando tests de base de datos...")
    
    # Crear base de datos temporal
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
        print("📋 Creando tablas...")
        models = DatabaseModels()
        models.initialize_database()
        
        # Test UserRepository
        print("👤 Test UserRepository...")
        user_repo = UserRepository()
        
        user_data = {
            'username': f'test_user_{hash(str(db_path)) % 10000}',  # Username único
            'password_hash': 'hashed_password',
            'role_id': 1,
            'is_active': True
        }
        
        user_id = user_repo.create(user_data)
        print(f"   ✅ Usuario creado con ID: {user_id}")
        
        retrieved_user = user_repo.get_by_id(user_id)
        print(f"   🔍 Debug: retrieved_user = {retrieved_user}")
        assert retrieved_user is not None, f"Usuario no encontrado con ID {user_id}"
        assert retrieved_user['username'] == user_data['username']
        print("   ✅ Usuario recuperado correctamente")
        
        # Test StudentRepository
        print("🎓 Test StudentRepository...")
        student_repo = StudentRepository()
        
        student_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'classroom_id': 1,
            'enrollment_status': 'activo',
            'tutor_name': 'María Pérez'
        }
        
        student_id = student_repo.create(student_data)
        print(f"   ✅ Estudiante creado con ID: {student_id}")
        
        retrieved_student = student_repo.get_by_id(student_id)
        assert retrieved_student is not None
        assert retrieved_student['first_name'] == 'Juan'
        print("   ✅ Estudiante recuperado correctamente")
        
        # Test búsqueda
        search_results = student_repo.search_by_name('Juan')
        assert len(search_results) > 0
        print("   ✅ Búsqueda por nombre funciona")
        
        print("🎉 Todos los tests pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restaurar path original
        config.DB_PATH = original_db_path
        database.connection.DB_PATH = original_db_path
        
        # Limpiar archivo temporal
        if db_path.exists():
            os.unlink(db_path)


if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
