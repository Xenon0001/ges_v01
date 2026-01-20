"""
SQLAlchemy models for person-related entities
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    SECRETARY = "secretary"
    TEACHER = "teacher"


class PersonModel(Base):
    """SQLAlchemy model for Person entity"""
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address = Column(String(300))
    birth_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("UserModel", back_populates="person")
    students = relationship("StudentModel", back_populates="person")
    tutors = relationship("TutorModel", back_populates="person")


class UserModel(Base):
    """SQLAlchemy model for User entity"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    person_id = Column(Integer, ForeignKey('persons.id'))
    school_id = Column(Integer, ForeignKey('schools.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    person = relationship("PersonModel", back_populates="users")
    school = relationship("SchoolModel", back_populates="users")


class StudentModel(Base):
    """SQLAlchemy model for Student entity"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(20), unique=True, nullable=False)
    enrollment_date = Column(Date)
    previous_school = Column(String(200))
    medical_info = Column(String(500))
    emergency_contact = Column(String(200))
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    person = relationship("PersonModel", back_populates="students")
    enrollments = relationship("EnrollmentModel", back_populates="student")


class TutorModel(Base):
    """SQLAlchemy model for Tutor entity"""
    __tablename__ = 'tutors'
    
    id = Column(Integer, primary_key=True)
    profession = Column(String(100))
    workplace = Column(String(200))
    id_number = Column(String(50))
    relationship_to_student = Column(String(50))
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    person = relationship("PersonModel", back_populates="tutors")
    enrollments = relationship("EnrollmentModel", back_populates="tutor")
