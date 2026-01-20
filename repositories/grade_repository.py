from typing import List, Optional, Dict
from database.models.school import GradeModel
from database.models.person import StudentModel
from .base_repository import BaseRepository


class GradeRepository(BaseRepository[GradeModel]):
    def __init__(self):
        super().__init__(GradeModel)
    
    def get_by_academic_year(self, academic_year: str) -> List[GradeModel]:
        session = self.get_session()
        try:
            return session.query(GradeModel).filter(
                GradeModel.academic_year == academic_year
            ).all()
        finally:
            self.close()
    
    def get_by_level(self, level: str) -> List[GradeModel]:
        session = self.get_session()
        try:
            return session.query(GradeModel).filter(GradeModel.level == level).all()
        finally:
            self.close()


class GradeRecordRepository(BaseRepository):
    """Placeholder - GradeRecordModel not implemented in new design"""
    def __init__(self):
        pass
    
    def get_student_grades(self, student_id: int, academic_year: str, trimester: Optional[int] = None) -> List:
        return []
    
    def get_subject_grades(self, subject_id: int, academic_year: str, trimester: Optional[int] = None) -> List:
        return []
