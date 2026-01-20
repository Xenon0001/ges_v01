"""
Domain entities for GES - Sistema de Gestión Escolar
Pure business entities without infrastructure dependencies
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    SECRETARY = "secretary"
    TEACHER = "teacher"


class EnrollmentStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"


class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


@dataclass
class School:
    """School entity - represents the educational institution"""
    id: Optional[int] = None
    name: str = ""
    code: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    principal_name: str = ""
    academic_year: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Person:
    """Base person entity"""
    id: Optional[int] = None
    name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.name} {self.last_name}"


@dataclass
class User(Person):
    """User entity with authentication"""
    username: str = ""
    password_hash: str = ""
    role: UserRole = UserRole.SECRETARY
    is_active: bool = True
    last_login: Optional[datetime] = None
    person_id: Optional[int] = None


@dataclass
class Student(Person):
    """Student entity"""
    student_id: str = ""
    enrollment_date: Optional[date] = None
    previous_school: Optional[str] = None
    medical_info: Optional[str] = None
    emergency_contact: Optional[str] = None
    
    def __post_init__(self):
        if not self.student_id:
            # Generate student ID if not provided
            self.student_id = f"EST{datetime.now().year:04d}"


@dataclass
class Tutor(Person):
    """Tutor entity - responsible for student"""
    profession: Optional[str] = None
    workplace: Optional[str] = None
    id_number: Optional[str] = None
    relationship_to_student: Optional[str] = None


@dataclass
class AcademicYear:
    """Academic year entity"""
    id: Optional[int] = None
    year: str = ""
    start_date: date = date.today()
    end_date: date = date.today()
    is_active: bool = True
    tuition_fee: float = 0.0
    registration_fee: float = 0.0
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.year:
            self.year = f"{self.start_date.year}-{self.end_date.year}"


@dataclass
class Grade:
    """Grade/Class level entity"""
    id: Optional[int] = None
    name: str = ""
    level: str = ""  # primary, secondary
    section: Optional[str] = None
    capacity: int = 30
    academic_year_id: int = 0
    classroom_id: Optional[int] = None
    tuition_fee: float = 0.0
    created_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        if self.section:
            return f"{self.name} {self.section}"
        return self.name


@dataclass
class Course:
    """Course/Subject entity"""
    id: Optional[int] = None
    name: str = ""
    code: str = ""
    description: Optional[str] = None
    credits: int = 1
    grade_id: int = 0
    is_mandatory: bool = True
    created_at: Optional[datetime] = None


@dataclass
class Classroom:
    """Physical classroom entity"""
    id: Optional[int] = None
    number: str = ""
    building: Optional[str] = None
    floor: Optional[str] = None
    capacity: int = 30
    has_projector: bool = False
    has_computers: bool = False
    is_active: bool = True
    created_at: Optional[datetime] = None


@dataclass
class Enrollment:
    """Student enrollment entity"""
    id: Optional[int] = None
    student_id: int = 0
    grade_id: int = 0
    academic_year_id: int = 0
    enrollment_date: date = date.today()
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE
    tutor_id: Optional[int] = None
    enrollment_number: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.enrollment_number:
            self.enrollment_number = f"MAT{datetime.now().strftime('%Y%m%d%H%M%S')}"


@dataclass
class Payment:
    """Payment entity for tuition and fees"""
    id: Optional[int] = None
    enrollment_id: int = 0
    amount: float = 0.0
    payment_date: Optional[date] = None
    due_date: date = date.today()
    status: PaymentStatus = PaymentStatus.PENDING
    payment_method: Optional[str] = None
    description: str = ""
    academic_year_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def is_overdue(self) -> bool:
        return self.status == PaymentStatus.PENDING and date.today() > self.due_date
