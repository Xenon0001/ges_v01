"""
SQLAlchemy models for school-related entities
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class SchoolModel(Base):
    """SQLAlchemy model for School entity"""
    __tablename__ = 'schools'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(String(300))
    phone = Column(String(20))
    email = Column(String(100))
    principal_name = Column(String(200))
    academic_year = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    academic_years = relationship("AcademicYearModel", back_populates="school")
    users = relationship("UserModel", back_populates="school")


class AcademicYearModel(Base):
    """SQLAlchemy model for AcademicYear entity"""
    __tablename__ = 'academic_years'
    
    id = Column(Integer, primary_key=True)
    year = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    tuition_fee = Column(Float, default=0.0)
    registration_fee = Column(Float, default=0.0)
    school_id = Column(Integer, ForeignKey('schools.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    school = relationship("SchoolModel", back_populates="academic_years")
    grades = relationship("GradeModel", back_populates="academic_year")
    enrollments = relationship("EnrollmentModel", back_populates="academic_year")
    payments = relationship("PaymentModel", back_populates="academic_year")


class GradeModel(Base):
    """SQLAlchemy model for Grade entity"""
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    level = Column(String(20), nullable=False)  # primary, secondary
    section = Column(String(20))
    capacity = Column(Integer, default=30)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False)
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    tuition_fee = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    academic_year = relationship("AcademicYearModel", back_populates="grades")
    classroom = relationship("ClassroomModel", back_populates="grades")
    courses = relationship("CourseModel", back_populates="grade")
    enrollments = relationship("EnrollmentModel", back_populates="grade")


class CourseModel(Base):
    """SQLAlchemy model for Course entity"""
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(String(500))
    credits = Column(Integer, default=1)
    grade_id = Column(Integer, ForeignKey('grades.id'), nullable=False)
    is_mandatory = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    grade = relationship("GradeModel", back_populates="courses")


class ClassroomModel(Base):
    """SQLAlchemy model for Classroom entity"""
    __tablename__ = 'classrooms'
    
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    building = Column(String(50))
    floor = Column(String(20))
    capacity = Column(Integer, default=30)
    has_projector = Column(Boolean, default=False)
    has_computers = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    grades = relationship("GradeModel", back_populates="classroom")
