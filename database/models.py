from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class PersonModel(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': 'discriminator'
    }
    
    discriminator = Column(String(50))
    
    # Relationships that will be inherited
    enrollments = relationship("EnrollmentModel", back_populates="student", viewonly=True)
    grade_records = relationship("GradeRecordModel", back_populates="student", viewonly=True)


class StudentModel(PersonModel):
    __tablename__ = 'students'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    student_id = Column(String(20), unique=True, nullable=False)
    birth_date = Column(Date)
    grade = Column(String(50))
    enrollment_date = Column(Date)
    
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }
    
    

class TutorModel(PersonModel):
    __tablename__ = 'tutors'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    profession = Column(String(100))
    relationship = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'tutor',
    }
    
    

class TeacherModel(PersonModel):
    __tablename__ = 'teachers'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    employee_id = Column(String(20), unique=True, nullable=False)
    specialization = Column(String(100))
    hire_date = Column(Date)
    
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }
    
    

class GradeModel(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    level = Column(String(20), nullable=False)  # primary, secondary
    section = Column(String(20))
    academic_year = Column(String(20), nullable=False)
    
    

class EnrollmentModel(Base):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    grade_id = Column(Integer, ForeignKey('grades.id'), nullable=False)
    academic_year = Column(String(20), nullable=False)
    enrollment_date = Column(Date)
    tutor_id = Column(Integer, ForeignKey('tutors.id'))
    status = Column(String(20), default='active')  # active, inactive, graduated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    

class SubjectModel(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    grade_id = Column(Integer, ForeignKey('grades.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    
    

class GradeRecordModel(Base):
    __tablename__ = 'grade_records'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    trimester = Column(Integer, nullable=False)
    grade_value = Column(Float, nullable=False)
    max_grade = Column(Float, default=10.0)
    academic_year = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    

class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, secretary, teacher
    person_id = Column(Integer, ForeignKey('persons.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    
