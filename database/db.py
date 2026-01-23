"""
Database configuration and setup for GES
SQLite database with SQLAlchemy ORM
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from datetime import datetime

# Import all models to ensure they are registered with Base
from database.models.base import Base
from database.models.school import SchoolModel, AcademicYearModel, GradeModel, CourseModel, ClassroomModel
from database.models.person import PersonModel, UserModel, StudentModel, TutorModel, UserRole
from database.models.enrollment import EnrollmentModel, PaymentModel, EnrollmentStatus, PaymentStatus

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ges_database.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging in development
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Get database session"""
    return SessionLocal


class DatabaseManager:
    """Database manager for GES application"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_tables(self):
        """Create all database tables"""
        try:
            # Create all tables from single Base
            Base.metadata.create_all(bind=self.engine)
            print("Database tables created successfully")
            return True
        except SQLAlchemyError as e:
            print(f"Error creating database tables: {e}")
            return False
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Close database session"""
        try:
            session.close()
        except Exception as e:
            print(f"Warning: Error closing session: {e}")
    
    def test_connection(self):
        """Test database connection"""
        try:
            session = self.get_session()
            session.execute(text("SELECT 1"))
            self.close_session(session)
            print("Database connection successful")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    # BORRAR EN PRODUCCIÓN --------------------------------------------------------------
    def initialize_sample_data(self):
        """Initialize sample data for testing"""
        try:
            session = self.get_session()
            
            # Check if data already exists
            if session.query(SchoolModel).first():
                print("Sample data already exists")
                self.close_session(session)
                return True
            
            # Create sample school
            school = SchoolModel(
                name="Colegio Ejemplo",
                code="CE001",
                address="Calle Principal, Ciudad",
                phone="+240 123 456 789",
                email="info@colegioejemplo.gq",
                principal_name="Dr. Juan Pérez",
                academic_year="2024-2025"
            )
            session.add(school)
            session.flush()  # Get the ID without committing
            
            # Create academic year
            academic_year = AcademicYearModel(
                year="2024-2025",
                start_date=datetime(2024, 9, 1),
                end_date=datetime(2025, 6, 30),
                is_active=True,
                tuition_fee=50000.0,
                registration_fee=5000.0,
                school_id=school.id
            )
            session.add(academic_year)
            session.flush()
            
            # Create sample classroom
            classroom = ClassroomModel(
                number="A-101",
                building="A",
                floor="1",
                capacity=30,
                has_projector=True,
                has_computers=False
            )
            session.add(classroom)
            session.flush()
            
            # Create sample grade
            grade = GradeModel(
                name="1º Primaria",
                level="primary",
                section="A",
                capacity=25,
                academic_year_id=academic_year.id,
                classroom_id=classroom.id,
                tuition_fee=50000.0
            )
            session.add(grade)
            session.flush()
            
            # Create sample course
            course = CourseModel(
                name="Matemáticas",
                code="MAT001",
                description="Matemáticas básicas",
                credits=2,
                grade_id=grade.id,
                is_mandatory=True
            )
            session.add(course)
            
            # Create admin user
            person = PersonModel(
                name="Admin",
                last_name="System",
                email="admin@colegioejemplo.gq",
                phone="+240 123 456 789"
            )
            session.add(person)
            session.flush()
            
            user = UserModel(
                username="admin",
                password_hash="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # 'password' SHA-256
                role=UserRole.ADMIN,
                is_active=True,
                person_id=person.id,
                school_id=school.id
            )
            session.add(user)
            
            session.commit()
            print("Sample data initialized successfully")
            print("Default login: username='admin', password='password'")
            
            self.close_session(session)
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error initializing sample data: {e}")
            self.close_session(session)
            return False


# Global database manager instance
db_manager = DatabaseManager()


def init_database():
    """Initialize database with tables and sample data"""
    print("Initializing GES Database...")
    
    db_manager = DatabaseManager()
    
    if not db_manager.create_tables():
        print("Failed to create database tables")
        return False
    
    # Create sample data
    if not db_manager.initialize_sample_data():
        print("Sample data already exists")
    
    print("Database initialization complete")
    return True


def get_db():
    """Dependency to get database session"""
    session = db_manager.get_session()
    try:
        yield session
    finally:
        db_manager.close_session(session)
