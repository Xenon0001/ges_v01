"""
Student service for GES application
Handles student management and business operations
"""

from typing import List, Optional
from datetime import date, datetime
from app.repositories.student_repository import StudentRepository, TutorRepository
from app.repositories.user_repository import PersonRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from database.models.person import StudentModel, PersonModel
from database.models.enrollment import EnrollmentModel
from app.domain.entities import Student, Tutor


class StudentService:
    """Service for student management operations"""
    
    def __init__(self):
        self.student_repo = StudentRepository()
        self.tutor_repo = TutorRepository()
        self.person_repo = PersonRepository()
        self.enrollment_repo = EnrollmentRepository()
    
    def create_student(self, student_data: dict) -> StudentModel:
        """Create new student with validation"""
        
        # Validate required fields
        required_fields = ['name', 'last_name', 'birth_date']
        for field in required_fields:
            if not student_data.get(field):
                raise ValueError(f"Field '{field}' is required")
        
        # Validate birth date
        birth_date = student_data['birth_date']
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        
        age = (date.today() - birth_date).days // 365
        if age < 3 or age > 65:
            raise ValueError("Student age must be between 3 and 65 years")
        
        # Check for duplicate student ID
        student_id = student_data.get('student_id') or self._generate_student_id()
        existing_student = self.student_repo.get_by_student_id(student_id)
        if existing_student:
            raise ValueError(f"Student ID '{student_id}' already exists")
        
        # Create person record
        person = PersonModel(
            name=student_data['name'],
            last_name=student_data['last_name'],
            email=student_data.get('email'),
            phone=student_data.get('phone'),
            address=student_data.get('address'),
            birth_date=birth_date
        )
        
        # This would normally be saved first, but for simplicity we'll create directly
        person.id = 1  # Placeholder ID
        
        # Create student record
        student = StudentModel(
            student_id=student_id,
            enrollment_date=student_data.get('enrollment_date', date.today()),
            previous_school=student_data.get('previous_school'),
            medical_info=student_data.get('medical_info'),
            emergency_contact=student_data.get('emergency_contact'),
            person_id=person.id
        )
        
        return self.student_repo.create(student)
    
    def _generate_student_id(self) -> str:
        """Generate unique student ID"""
        import time
        timestamp = str(int(time.time()))
        return f"EST{timestamp}"
    
    def get_student_by_id(self, student_id: int) -> Optional[StudentModel]:
        """Get student by database ID"""
        return self.student_repo.get_by_id(student_id)
    
    def get_student_by_student_id(self, student_id: str) -> Optional[StudentModel]:
        """Get student by student ID (e.g., 'EST001')"""
        return self.student_repo.get_by_student_id(student_id)
    
    def search_students(self, name: str = None, student_id: str = None) -> List[StudentModel]:
        """Search students by name or student ID"""
        return self.student_repo.search(name, student_id)
    
    def get_students_by_grade(self, grade_id: int) -> List[StudentModel]:
        """Get all active students in a grade"""
        return self.student_repo.get_by_grade(grade_id)
    
    def update_student(self, student_id: int, update_data: dict) -> StudentModel:
        """Update student information"""
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found")
        
        # Update fields
        for field, value in update_data.items():
            if hasattr(student, field) and value is not None:
                setattr(student, field, value)
        
        return self.student_repo.update(student)
    
    def get_student_academic_history(self, student_id: int) -> List[EnrollmentModel]:
        """Get student's academic enrollment history"""
        return self.enrollment_repo.get_by_student_and_year(student_id, None)
    
    def is_student_enrollable(self, student_id: int, academic_year_id: int) -> bool:
        """Check if student can be enrolled in academic year"""
        # Check if already enrolled
        if self.student_repo.is_enrolled_in_year(student_id, academic_year_id):
            return False
        
        # Check student status (could add more business rules)
        student = self.student_repo.get_by_id(student_id)
        if not student:
            return False
        
        return True
    
    def get_student_statistics(self, grade_id: int = None) -> dict:
        """Get student statistics"""
        if grade_id:
            students = self.student_repo.get_by_grade(grade_id)
        else:
            students = self.student_repo.get_all()
        
        # Calculate age statistics
        ages = []
        for student in students:
            if student.person and student.person.birth_date:
                age = (date.today() - student.person.birth_date).days // 365
                ages.append(age)
        
        return {
            'total_students': len(students),
            'average_age': sum(ages) / len(ages) if ages else 0,
            'age_range': {
                'min': min(ages) if ages else 0,
                'max': max(ages) if ages else 0
            },
            'enrollment_status': {
                'active': len([s for s in students if self._has_active_enrollment(s.id)]),
                'inactive': len([s for s in students if not self._has_active_enrollment(s.id)])
            }
        }
    
    def _has_active_enrollment(self, student_id: int) -> bool:
        """Check if student has active enrollment"""
        enrollments = self.enrollment_repo.get_by_student_and_year(student_id, None)
        return any(e.status == 'active' for e in enrollments)
    
    def delete_student(self, student_id: int) -> bool:
        """Delete student (soft delete recommended)"""
        try:
            # Check if student has active enrollments
            enrollments = self.enrollment_repo.get_by_student_and_year(student_id, None)
            active_enrollments = [e for e in enrollments if e.status == 'active']
            
            if active_enrollments:
                raise ValueError("Cannot delete student with active enrollments")
            
            return self.student_repo.delete(student_id)
        except Exception:
            return False
