from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List


@dataclass
class Person:
    id: Optional[int] = None
    name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Student(Person):
    student_id: str = ""
    birth_date: Optional[date] = None
    grade: Optional[str] = None
    enrollment_date: Optional[date] = None


@dataclass
class Tutor(Person):
    profession: Optional[str] = None
    relationship: Optional[str] = None


@dataclass
class Teacher(Person):
    employee_id: str = ""
    specialization: Optional[str] = None
    hire_date: Optional[date] = None


@dataclass
class Enrollment:
    id: Optional[int] = None
    student_id: int = 0
    grade_id: int = 0
    academic_year: str = ""
    enrollment_date: Optional[date] = None
    tutor_id: Optional[int] = None
    status: str = "active"  # active, inactive, graduated
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Grade:
    id: Optional[int] = None
    name: str = ""
    level: str = ""  # primary, secondary
    section: Optional[str] = None
    academic_year: str = ""


@dataclass
class Subject:
    id: Optional[int] = None
    name: str = ""
    code: str = ""
    grade_id: int = 0
    teacher_id: Optional[int] = None


@dataclass
class GradeRecord:
    id: Optional[int] = None
    student_id: int = 0
    subject_id: int = 0
    trimester: int = 1
    grade_value: float = 0.0
    max_grade: float = 10.0
    academic_year: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def is_passed(self) -> bool:
        return self.grade_value >= 5.0


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = ""  # admin, secretary, teacher
    person_id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
