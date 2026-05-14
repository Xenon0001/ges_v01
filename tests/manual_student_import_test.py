import sys
import tempfile
import importlib
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

import database.connection as db_conn_mod
from database.connection import DatabaseConnection

# Crear base de datos temporal y recargar módulos con el DB_PATH correcto
with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
    temp_db_path = Path(temp_file.name)

# Parchear config y database.connection antes de importar módulos que dependen de la DB
import config
config.DB_PATH = temp_db_path
importlib.reload(db_conn_mod)
from database.connection import db

import database.models as db_models_mod
importlib.reload(db_models_mod)
from database.models import DatabaseModels

import database.repository as db_repo_mod
importlib.reload(db_repo_mod)

models = DatabaseModels()
models.create_tables()
models.insert_initial_data()

from utils.initialize_default_structure import initialize_default_academic_structure
initialize_default_academic_structure()

from services.student_import_service import StudentImportService
from openpyxl import Workbook

xlsx_path = root / 'tests' / 'temp_student_import.xlsx'
wb = Workbook()
ws = wb.active
ws.title = 'Importación de Estudiantes'
headers = ['Nombre', 'Apellido', 'Curso', 'Aula', 'Turno', 'Tutor', 'Matrícula', 'Género', 'FechaNacimiento', 'Teléfono', 'Año Escolar']
ws.append(headers)
ws.append(['María', 'López', 'Primero', 'A', 'Mañana', 'Carlos López', '2024-001', 'F', '2014-05-20', '612345678', 2024])
ws.append(['José', 'Martínez', 'Segundo', 'A', 'Mañana', 'Ana Pérez', '2024-002', 'M', '2013-08-10', '612345679', 2024])
wb.save(xlsx_path)

svc = StudentImportService()
valid, msg = svc.validate_structure(str(xlsx_path))
print('validate_structure:', valid, msg)
result = svc.import_from_excel(str(xlsx_path))
print('total_rows:', result.total_rows)
print('imported_count:', result.imported_count)
print('omitted_count:', result.omitted_count)
print('error_count:', result.error_count)
print('errors:', [e.__dict__ for e in result.errors])
print('success_rows:', [s.__dict__ for s in result.success_rows])

rows = db_conn_mod.db.execute_query('SELECT * FROM students')
print('students in temp DB:', len(rows))
for row in rows:
    print(dict(row))

# Cleanup
xlsx_path.unlink(missing_ok=True)
temp_db_path.unlink(missing_ok=True)
