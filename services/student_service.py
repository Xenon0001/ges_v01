from typing import List, Optional
from datetime import date, datetime
from repositories.student_repository import StudentRepository
from repositories.grade_repository import GradeRecordRepository
from database.models.person import StudentModel
from domain.entities import Student, GradeRecord


class StudentService:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.grade_record_repo = GradeRecordRepository()
    
    def create_student(self, student: Student) -> StudentModel:
        """Create new student"""
        student_model = StudentModel(
            name=student.name,
            last_name=student.last_name,
            email=student.email,
            phone=student.phone,
            address=student.address,
            student_id=student.student_id,
            birth_date=student.birth_date,
            grade=student.grade,
            enrollment_date=student.enrollment_date or date.today()
        )
        
        return self.student_repo.create(student_model)
    
    def get_student_by_id(self, student_id: int) -> Optional[StudentModel]:
        """Get student by database ID"""
        return self.student_repo.get_by_id(student_id)
    
    def get_student_by_student_id(self, student_id: str) -> Optional[StudentModel]:
        """Get student by student ID (e.g., 'EST001')"""
        return self.student_repo.get_by_student_id(student_id)
    
    def get_all_students(self) -> List[StudentModel]:
        """Get all students"""
        return self.student_repo.get_all()
    
    def get_students_by_grade(self, grade_id: int) -> List[StudentModel]:
        """Get students by grade"""
        return self.student_repo.get_by_grade(grade_id)
    
    def update_student(self, student: StudentModel) -> StudentModel:
        """Update student information"""
        return self.student_repo.update(student)
    
    def add_grade_record(self, grade_record: GradeRecord):
        """Add grade record for student - placeholder"""
        # Placeholder - GradeRecordModel not implemented in new design
        pass
    
    def get_student_grades(self, student_id: int, academic_year: str, trimester: Optional[int] = None) -> List:
        """Get student's grade records"""
        return self.grade_record_repo.get_student_grades(student_id, academic_year, trimester)
    
    def calculate_student_average(self, student_id: int, academic_year: str, trimester: Optional[int] = None) -> float:
        """Calculate student's average grade"""
        grades = self.get_student_grades(student_id, academic_year, trimester)
        
        if not grades:
            return 0.0
        
        total = sum(grade.grade_value for grade in grades)
        return total / len(grades)
    
    def is_student_passed(self, student_id: int, academic_year: str) -> bool:
        """Check if student passed the academic year"""
        average = self.calculate_student_average(student_id, academic_year)
        return average >= 5.0
