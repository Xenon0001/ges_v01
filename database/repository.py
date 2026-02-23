"""
Repository layer para GES
Operaciones CRUD de base de datos para todas las entidades
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from database.connection import db
from config import TABLES


class BaseRepository:
    """Repository base con operaciones CRUD comunes"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.table = TABLES[table_name]
    
    def create(self, data: Dict[str, Any]) -> int:
        """Inserta un nuevo registro y devuelve el ID"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        
        # Usar la conexión directamente para obtener el ID inmediatamente
        with db.get_connection() as conn:
            cursor = conn.execute(query, values)
            insert_id = cursor.lastrowid
        return insert_id if insert_id else 0
    
    def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un registro por ID"""
        query = f"SELECT * FROM {self.table} WHERE id = ?"
        results = db.execute_query(query, (record_id,))
        return results[0] if results else None
    
    def get_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los registros"""
        query = f"SELECT * FROM {self.table}"
        if limit:
            query += f" LIMIT {limit}"
        return db.execute_query(query)
    
    def update(self, record_id: int, data: Dict[str, Any]) -> int:
        """Actualiza un registro y devuelve el número de filas afectadas"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (record_id,)
        
        query = f"UPDATE {self.table} SET {set_clause} WHERE id = ?"
        return db.execute_update(query, values)
    
    def delete(self, record_id: int) -> int:
        """Elimina un registro y devuelve el número de filas afectadas"""
        query = f"DELETE FROM {self.table} WHERE id = ?"
        return db.execute_update(query, (record_id,))
    
    def find_by(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """Busca registros por un campo específico"""
        query = f"SELECT * FROM {self.table} WHERE {field} = ?"
        return db.execute_query(query, (value,))


class UserRepository(BaseRepository):
    """Repository para usuarios"""
    
    def __init__(self):
        super().__init__('users')
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por nombre de usuario"""
        results = self.find_by('username', username)
        return results[0] if results else None
    
    def get_active_users(self) -> List[Dict[str, Any]]:
        """Obtiene usuarios activos"""
        query = f"SELECT * FROM {self.table} WHERE is_active = 1"
        return db.execute_query(query)
    
    def get_users_by_role(self, role_id: int) -> List[Dict[str, Any]]:
        """Obtiene usuarios por rol"""
        query = f"""
            SELECT u.*, r.name as role_name 
            FROM {self.table} u 
            JOIN {TABLES['roles']} r ON u.role_id = r.id 
            WHERE u.role_id = ?
        """
        return db.execute_query(query, (role_id,))


class StudentRepository(BaseRepository):
    """Repository para estudiantes"""
    
    def __init__(self):
        super().__init__('students')
    
    def get_by_classroom(self, classroom_id: int) -> List[Dict[str, Any]]:
        """Obtiene estudiantes por aula"""
        return self.find_by('classroom_id', classroom_id)
    
    def get_active_students(self) -> List[Dict[str, Any]]:
        """Obtiene estudiantes activos"""
        return self.find_by('enrollment_status', 'activo')
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Busca estudiantes por nombre"""
        query = f"""
            SELECT * FROM {self.table} 
            WHERE first_name LIKE ? OR last_name LIKE ?
        """
        pattern = f"%{name}%"
        return db.execute_query(query, (pattern, pattern))
    
    def get_with_classroom(self, student_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene estudiante con información del aula"""
        query = f"""
            SELECT s.*, c.name as classroom_name, g.name as grade_name, l.name as level_name
            FROM {self.table} s
            LEFT JOIN {TABLES['classrooms']} c ON s.classroom_id = c.id
            LEFT JOIN {TABLES['grades']} g ON c.grade_id = g.id
            LEFT JOIN {TABLES['levels']} l ON g.level_id = l.id
            WHERE s.id = ?
        """
        results = db.execute_query(query, (student_id,))
        return results[0] if results else None


class ScoreRepository(BaseRepository):
    """Repository para calificaciones"""
    
    def __init__(self):
        super().__init__('scores')
    
    def get_by_student(self, student_id: int, academic_year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtiene calificaciones de un estudiante"""
        if academic_year:
            query = f"""
                SELECT sc.*, sub.name as subject_name, t.name as teacher_name
                FROM {self.table} sc
                JOIN {TABLES['subjects']} sub ON sc.subject_id = sub.id
                JOIN {TABLES['teachers']} t ON sc.teacher_id = t.id
                WHERE sc.student_id = ? AND sc.academic_year = ?
                ORDER BY sc.trimester, sub.name
            """
            return db.execute_query(query, (student_id, academic_year))
        else:
            query = f"""
                SELECT sc.*, sub.name as subject_name, t.name as teacher_name
                FROM {self.table} sc
                JOIN {TABLES['subjects']} sub ON sc.subject_id = sub.id
                JOIN {TABLES['teachers']} t ON sc.teacher_id = t.id
                WHERE sc.student_id = ?
                ORDER BY sc.academic_year, sc.trimester, sub.name
            """
            return db.execute_query(query, (student_id,))
    
    def get_by_subject(self, subject_id: int, trimester: int, academic_year: int) -> List[Dict[str, Any]]:
        """Obtiene calificaciones por materia, trimestre y año"""
        query = f"""
            SELECT sc.*, s.first_name, s.last_name
            FROM {self.table} sc
            JOIN {TABLES['students']} s ON sc.student_id = s.id
            WHERE sc.subject_id = ? AND sc.trimester = ? AND sc.academic_year = ?
            ORDER BY s.last_name, s.first_name
        """
        return db.execute_query(query, (subject_id, trimester, academic_year))
    
    def get_student_average(self, student_id: int, academic_year: int, trimester: Optional[int] = None) -> Optional[float]:
        """Calcula el promedio de un estudiante"""
        if trimester:
            query = f"""
                SELECT AVG(sc.score) as average
                FROM {self.table} sc
                WHERE sc.student_id = ? AND sc.academic_year = ? AND sc.trimester = ?
                AND sc.score IS NOT NULL
            """
            result = db.execute_query(query, (student_id, academic_year, trimester))
        else:
            query = f"""
                SELECT AVG(sc.score) as average
                FROM {self.table} sc
                WHERE sc.student_id = ? AND sc.academic_year = ?
                AND sc.score IS NOT NULL
            """
            result = db.execute_query(query, (student_id, academic_year))
        
        return result[0]['average'] if result and result[0]['average'] else None


class PaymentRepository(BaseRepository):
    """Repository para pagos"""
    
    def __init__(self):
        super().__init__('payments')
    
    def get_by_student(self, student_id: int) -> List[Dict[str, Any]]:
        """Obtiene pagos de un estudiante"""
        return self.find_by('student_id', student_id)
    
    def get_pending_payments(self) -> List[Dict[str, Any]]:
        """Obtiene pagos pendientes"""
        query = f"""
            SELECT p.*, s.first_name, s.last_name
            FROM {self.table} p
            JOIN {TABLES['students']} s ON p.student_id = s.id
            WHERE p.status = 'pendiente' OR p.status = 'retrasado'
            ORDER BY p.due_date
        """
        return db.execute_query(query)
    
    def get_overdue_payments(self) -> List[Dict[str, Any]]:
        """Obtiene pagos vencidos"""
        today = date.today().isoformat()
        query = f"""
            SELECT p.*, s.first_name, s.last_name
            FROM {self.table} p
            JOIN {TABLES['students']} s ON p.student_id = s.id
            WHERE p.due_date < ? AND p.status != 'pagado'
            ORDER BY p.due_date
        """
        return db.execute_query(query, (today,))
    
    def get_debt_summary(self, student_id: int) -> Dict[str, float]:
        """Obtiene resumen de deuda de un estudiante"""
        query = f"""
            SELECT 
                SUM(amount_due) as total_due,
                SUM(amount_paid) as total_paid,
                SUM(CASE WHEN status != 'pagado' THEN (amount_due - amount_paid) ELSE 0 END) as outstanding
            FROM {self.table}
            WHERE student_id = ?
        """
        result = db.execute_query(query, (student_id,))
        return result[0] if result else {'total_due': 0.0, 'total_paid': 0.0, 'outstanding': 0.0}


class SubjectRepository(BaseRepository):
    """Repository para materias"""
    
    def __init__(self):
        super().__init__('subjects')
    
    def get_with_teachers(self) -> List[Dict[str, Any]]:
        """Obtiene materias con sus profesores"""
        query = f"""
            SELECT sub.*, t.name as teacher_name
            FROM {self.table} sub
            LEFT JOIN {TABLES['teachers']} t ON sub.id = t.subject_id
            ORDER BY sub.name
        """
        return db.execute_query(query)


class ClassroomRepository(BaseRepository):
    """Repository para aulas"""
    
    def __init__(self):
        super().__init__('classrooms')
    
    def get_with_details(self) -> List[Dict[str, Any]]:
        """Obtiene aulas con detalles de grado y nivel"""
        query = f"""
            SELECT c.*, g.name as grade_name, l.name as level_name
            FROM {self.table} c
            JOIN {TABLES['grades']} g ON c.grade_id = g.id
            JOIN {TABLES['levels']} l ON g.level_id = l.id
            ORDER BY l.name, g.name, c.name
        """
        return db.execute_query(query)
    
    def get_student_count(self, classroom_id: int) -> int:
        """Obtiene número de estudiantes en un aula"""
        query = f"""
            SELECT COUNT(*) as count
            FROM {TABLES['students']}
            WHERE classroom_id = ? AND enrollment_status = 'activo'
        """
        result = db.execute_query(query, (classroom_id,))
        return result[0]['count'] if result else 0


# Instancias de repositories
user_repo = UserRepository()
student_repo = StudentRepository()
score_repo = ScoreRepository()
payment_repo = PaymentRepository()
subject_repo = SubjectRepository()
classroom_repo = ClassroomRepository()

# Repository para teachers (basado en BaseRepository)
class TeacherRepository(BaseRepository):
    """Repository para profesores"""
    
    def __init__(self):
        super().__init__('teachers')
    
    def get_by_subject(self, subject_id: int) -> List[Dict[str, Any]]:
        """Obtiene profesores por materia"""
        return self.find_by('subject_id', subject_id)

teacher_repo = TeacherRepository()
