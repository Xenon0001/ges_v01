from typing import List, Optional
from database.models.person import StudentModel
from database.models.enrollment import EnrollmentModel
from .base_repository import BaseRepository


class StudentRepository(BaseRepository[StudentModel]):
    def __init__(self):
        super().__init__(StudentModel)
    
    def get_by_student_id(self, student_id: str) -> Optional[StudentModel]:
        session = self.get_session()
        try:
            return session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        finally:
            self.close()
    
    def get_by_grade(self, grade_id: int) -> List[StudentModel]:
        session = self.get_session()
        try:
            return session.query(StudentModel).join(EnrollmentModel).filter(
                EnrollmentModel.grade_id == grade_id,
                EnrollmentModel.status == 'active'
            ).all()
        finally:
            self.close()
    
    def get_enrollments(self, student_id: int) -> List[EnrollmentModel]:
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.student_id == student_id
            ).all()
        finally:
            self.close()
    
    def get_grade_records(self, student_id: int, academic_year: Optional[str] = None) -> List:
        # Placeholder - GradeRecordModel not implemented in new design
        return []
