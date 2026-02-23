"""
Modelos de base de datos para GES
Definiciones de tablas y esquemas según el modelo oficial
"""

from typing import List, Dict, Any
from database.connection import db
from config import TABLES


class DatabaseModels:
    """Gestiona la creación y validación de la estructura de la base de datos"""
    
    @staticmethod
    def create_tables() -> None:
        """Crea todas las tablas necesarias para GES"""
        
        # Tabla schools
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['schools']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT,
                year_active INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla roles
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['roles']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                permissions TEXT
            )
        """)
        
        # Tabla users
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['users']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES {TABLES['roles']} (id)
            )
        """)
        
        # Tabla levels
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['levels']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        
        # Tabla grades
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['grades']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level_id INTEGER,
                name TEXT NOT NULL,
                FOREIGN KEY (level_id) REFERENCES {TABLES['levels']} (id)
            )
        """)
        
        # Tabla classrooms
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['classrooms']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade_id INTEGER,
                name TEXT NOT NULL,
                shift TEXT DEFAULT 'Mañana',
                FOREIGN KEY (grade_id) REFERENCES {TABLES['grades']} (id)
            )
        """)
        
        # Tabla subjects
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['subjects']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        
        # Tabla teachers
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['teachers']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject_id INTEGER,
                FOREIGN KEY (subject_id) REFERENCES {TABLES['subjects']} (id)
            )
        """)
        
        # Tabla students
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['students']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                classroom_id INTEGER,
                enrollment_status TEXT DEFAULT 'activo',
                tutor_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (classroom_id) REFERENCES {TABLES['classrooms']} (id)
            )
        """)
        
        # Tabla scores
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['scores']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                teacher_id INTEGER NOT NULL,
                trimester INTEGER CHECK(trimester IN (1, 2, 3)),
                score REAL,
                recovery_score REAL,
                academic_year INTEGER,
                FOREIGN KEY (student_id) REFERENCES {TABLES['students']} (id),
                FOREIGN KEY (subject_id) REFERENCES {TABLES['subjects']} (id),
                FOREIGN KEY (teacher_id) REFERENCES {TABLES['teachers']} (id)
            )
        """)
        
        # Tabla payments
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['payments']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                amount_due REAL NOT NULL,
                amount_paid REAL DEFAULT 0,
                due_date DATE,
                status TEXT DEFAULT 'pendiente',
                calendar_group TEXT,
                FOREIGN KEY (student_id) REFERENCES {TABLES['students']} (id)
            )
        """)
        
        # Tabla alerts
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['alerts']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                reference_id INTEGER,
                message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla history
        db.execute_update(f"""
            CREATE TABLE IF NOT EXISTS {TABLES['history']} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES {TABLES['users']} (id)
            )
        """)
    
    @staticmethod
    def insert_initial_data() -> None:
        """Inserta datos iniciales necesarios para el funcionamiento"""
        
        # Roles básicos
        roles = [
            ('Directiva', '{"view_dashboard": true, "edit_students": true, "view_finances": true, "manage_users": true}'),
            ('Secretaria', '{"view_dashboard": true, "edit_students": true, "view_finances": true, "manage_users": false}'),
            ('Usuario', '{"view_dashboard": false, "edit_students": false, "view_finances": false, "manage_users": false}')
        ]
        
        db.execute_many(f"""
            INSERT OR IGNORE INTO {TABLES['roles']} (name, permissions) VALUES (?, ?)
        """, roles)
        
        # Niveles educativos
        levels = [
            ('Primaria',),
            ('Secundaria',),
            ('Bachillerato',)
        ]
        
        db.execute_many(f"""
            INSERT OR IGNORE INTO {TABLES['levels']} (name) VALUES (?)
        """, levels)
        
        # Materias básicas
        subjects = [
            ('Matemáticas',),
            ('Lenguaje',),
            ('Ciencias',),
            ('Historia',),
            ('Geografía',),
            ('Inglés',)
        ]
        
        db.execute_many(f"""
            INSERT OR IGNORE INTO {TABLES['subjects']} (name) VALUES (?)
        """, subjects)
    
    @staticmethod
    def initialize_database() -> None:
        """Inicializa la base de datos completa"""
        DatabaseModels.create_tables()
        DatabaseModels.insert_initial_data()


# Esquemas para validación
TABLE_SCHEMAS = {
    'users': {
        'required_fields': ['username', 'password_hash', 'role_id'],
        'field_types': {
            'username': str,
            'password_hash': str,
            'role_id': int,
            'is_active': bool
        }
    },
    'students': {
        'required_fields': ['first_name', 'last_name'],
        'field_types': {
            'first_name': str,
            'last_name': str,
            'classroom_id': int,
            'enrollment_status': str,
            'tutor_name': str
        }
    },
    'scores': {
        'required_fields': ['student_id', 'subject_id', 'teacher_id', 'trimester', 'academic_year'],
        'field_types': {
            'student_id': int,
            'subject_id': int,
            'teacher_id': int,
            'trimester': int,
            'score': float,
            'recovery_score': float,
            'academic_year': int
        }
    },
    'payments': {
        'required_fields': ['student_id', 'amount_due'],
        'field_types': {
            'student_id': int,
            'amount_due': float,
            'amount_paid': float,
            'due_date': str,
            'status': str,
            'calendar_group': str
        }
    }
}
