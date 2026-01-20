"""
Enrollment service for GES application
Handles student enrollment and business rules
"""

from typing import List, Optional
from datetime import date, datetime
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.school_repository import GradeRepository, AcademicYearRepository
from database.models.enrollment import EnrollmentModel
from database.models.person import StudentModel
from database.models.school import GradeModel, AcademicYearModel
from app.domain.entities import Enrollment, Student


class EnrollmentService:
    """Service for student enrollment operations"""
    
    def __init__(self):
        self.enrollment_repo = EnrollmentRepository()
        self.student_repo = StudentRepository()
        self.grade_repo = GradeRepository()
        self.academic_year_repo = AcademicYearRepository()
    
    def enroll_student(self, student_id: int, grade_id: int, academic_year_id: int, 
                    tutor_id: Optional[int] = None) -> EnrollmentModel:
        """Enroll student with business validation"""
        
        # Validate inputs
        if not all([student_id, grade_id, academic_year_id]):
            raise ValueError("Student ID, Grade ID, and Academic Year ID are required")
        
        # Check if student exists
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found")
        
        # Check if grade exists
        grade = self.grade_repo.get_by_id(grade_id)
        if not grade:
            raise ValueError("Grade not found")
        
        # Check if academic year exists
        academic_year = self.academic_year_repo.get_by_id(academic_year_id)
        if not academic_year:
            raise ValueError("Academic year not found")
        
        # BUSINESS RULE: Student cannot enroll twice in same academic year
        if self.student_repo.is_enrolled_in_year(student_id, academic_year_id):
            raise ValueError(f"Student {student.student_id} is already enrolled in academic year {academic_year.year}")
        
        # Check grade capacity
        current_enrollments = self.enrollment_repo.get_by_grade(grade_id)
        if len(current_enrollments) >= grade.capacity:
            raise ValueError(f"Grade {grade.name} has reached maximum capacity")
        
        # Create enrollment
        enrollment = EnrollmentModel(
            student_id=student_id,
            grade_id=grade_id,
            academic_year_id=academic_year_id,
            enrollment_date=date.today(),
            tutor_id=tutor_id,
            enrollment_number=self._generate_enrollment_number()
        )
        
        return self.enrollment_repo.create(enrollment)
    
    def _generate_enrollment_number(self) -> str:
        """Generate unique enrollment number"""
        import time
        timestamp = str(int(time.time()))
        return f"MAT{timestamp}"
    
    def get_student_enrollments(self, student_id: int) -> List[EnrollmentModel]:
        """Get all enrollments for a student"""
        return self.enrollment_repo.get_by_student_and_year(student_id, None)
    
    def get_grade_enrollments(self, grade_id: int) -> List[EnrollmentModel]:
        """Get all active enrollments for a grade"""
        return self.enrollment_repo.get_by_grade(grade_id)
    
    def get_tutor_enrollments(self, tutor_id: int) -> List[EnrollmentModel]:
        """Get all enrollments for a tutor"""
        return self.enrollment_repo.get_by_tutor(tutor_id)
    
    def update_enrollment_status(self, enrollment_id: int, status: str) -> bool:
        """Update enrollment status with validation"""
        from database.models.enrollment import EnrollmentStatus
        valid_statuses = [s.value for s in EnrollmentStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        try:
            self.enrollment_repo.update_status(enrollment_id, status)
            return True
        except Exception:
            return False
    
    def transfer_student(self, enrollment_id: int, new_grade_id: int) -> bool:
        """Transfer student to different grade"""
        # Get current enrollment
        enrollment = self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            return False
        
        # Check new grade capacity
        new_grade = self.grade_repo.get_by_id(new_grade_id)
        if not new_grade:
            raise ValueError("New grade not found")
        
        current_enrollments = self.enrollment_repo.get_by_grade(new_grade_id)
        if len(current_enrollments) >= new_grade.capacity:
            raise ValueError(f"Grade {new_grade.name} has reached maximum capacity")
        
        # Update enrollment
        enrollment.grade_id = new_grade_id
        self.enrollment_repo.update(enrollment)
        return True
    
    def get_enrollment_statistics(self, grade_id: int) -> dict:
        """Get enrollment statistics for a grade"""
        enrollments = self.enrollment_repo.get_by_grade(grade_id)
        grade = self.grade_repo.get_by_id(grade_id)
        
        return {
            'total_enrolled': len(enrollments),
            'capacity': grade.capacity if grade else 0,
            'available_spots': (grade.capacity - len(enrollments)) if grade else 0,
            'enrollment_rate': (len(enrollments) / grade.capacity * 100) if grade and grade.capacity > 0 else 0
        }
