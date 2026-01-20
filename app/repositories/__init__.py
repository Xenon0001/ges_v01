"""
Repositories package for GES application
Data access layer
"""

from .base_repository import BaseRepository
from .school_repository import SchoolRepository, AcademicYearRepository, GradeRepository, CourseRepository, ClassroomRepository
from .user_repository import UserRepository, PersonRepository
from .student_repository import StudentRepository
from .enrollment_repository import EnrollmentRepository, PaymentRepository

__all__ = [
    "BaseRepository",
    "SchoolRepository",
    "AcademicYearRepository",
    "GradeRepository",
    "CourseRepository",
    "ClassroomRepository",
    "UserRepository", 
    "PersonRepository",
    "StudentRepository",
    "EnrollmentRepository",
    "PaymentRepository"
]
