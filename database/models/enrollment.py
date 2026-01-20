"""
SQLAlchemy models for enrollment and payment entities
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base


class EnrollmentStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class EnrollmentModel(Base):
    """SQLAlchemy model for Enrollment entity"""
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    grade_id = Column(Integer, ForeignKey('grades.id'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    tutor_id = Column(Integer, ForeignKey('tutors.id'))
    enrollment_number = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("StudentModel", back_populates="enrollments")
    grade = relationship("GradeModel", back_populates="enrollments")
    academic_year = relationship("AcademicYearModel", back_populates="enrollments")
    tutor = relationship("TutorModel", back_populates="enrollments")
    payments = relationship("PaymentModel", back_populates="enrollment")


class PaymentModel(Base):
    """SQLAlchemy model for Payment entity"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(String(50))
    description = Column(String(200))
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollment = relationship("EnrollmentModel", back_populates="payments")
    academic_year = relationship("AcademicYearModel", back_populates="payments")
