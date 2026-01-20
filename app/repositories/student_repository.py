"""
Student repository for GES application
Handles student-related data operations
"""

from typing import List, Optional
from database.models.person import StudentModel, PersonModel
from database.models.enrollment import EnrollmentModel
from .base_repository import BaseRepository


class StudentRepository(BaseRepository[StudentModel]):
    """Repository for Student operations"""
    
    def __init__(self):
        super().__init__(StudentModel)
    
    def get_by_student_id(self, student_id: str) -> Optional[StudentModel]:
        """Get student by student ID (e.g., 'EST001')"""
        session = self.get_session()
        try:
            return session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        finally:
            pass
    
    def get_by_grade(self, grade_id: int) -> List[StudentModel]:
        """Get students by grade through enrollments"""
        session = self.get_session()
        try:
            return session.query(StudentModel).join(EnrollmentModel).filter(
                EnrollmentModel.grade_id == grade_id,
                EnrollmentModel.status == 'active'
            ).all()
        finally:
            pass
    
    def get_enrollments(self, student_id: int) -> List[EnrollmentModel]:
        """Get student's enrollments"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.student_id == student_id
            ).all()
        finally:
            pass
    
    def is_enrolled_in_year(self, student_id: int, academic_year_id: int) -> bool:
        """Check if student is enrolled in specific academic year"""
        session = self.get_session()
        try:
            enrollment = session.query(EnrollmentModel).filter(
                EnrollmentModel.student_id == student_id,
                EnrollmentModel.academic_year_id == academic_year_id
            ).first()
            return enrollment is not None
        finally:
            pass
    
    def search(self, name: str = None, student_id: str = None) -> List[StudentModel]:
        """Search students by name or student ID"""
        session = self.get_session()
        try:
            query = session.query(StudentModel).join(PersonModel)
            
            if name:
                query = query.filter(
                    PersonModel.name.ilike(f"%{name}%")
                )
            
            if student_id:
                query = query.filter(
                    StudentModel.student_id.ilike(f"%{student_id}%")
                )
            
            return query.all()
        finally:
            pass


class TutorRepository(BaseRepository[StudentModel]):
    """Repository for Tutor operations"""
    
    def __init__(self):
        super().__init__(StudentModel)
    
    def get_by_relationship(self, relationship: str) -> List:
        """Get tutors by relationship type"""
        session = self.get_session()
        try:
            return session.query(StudentModel).filter(
                StudentModel.relationship_to_student == relationship
            ).all()
        finally:
            pass
    
    def get_students_by_tutor(self, tutor_id: int) -> List[EnrollmentModel]:
        """Get students assigned to a tutor"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.tutor_id == tutor_id,
                EnrollmentModel.status == 'active'
            ).all()
        finally:
            pass
