"""
School repository for GES application
Handles school-related data operations
"""

from typing import List, Optional
from database.models.school import SchoolModel, AcademicYearModel, GradeModel, CourseModel, ClassroomModel
from .base_repository import BaseRepository


class SchoolRepository(BaseRepository[SchoolModel]):
    """Repository for School operations"""
    
    def __init__(self):
        super().__init__(SchoolModel)
    
    def get_by_code(self, code: str) -> Optional[SchoolModel]:
        """Get school by code"""
        session = self.get_session()
        try:
            return session.query(SchoolModel).filter(SchoolModel.code == code).first()
        finally:
            pass  # Session managed by context manager
    
    def get_active_academic_year(self, school_id: int) -> Optional[AcademicYearModel]:
        """Get active academic year for school"""
        session = self.get_session()
        try:
            return session.query(AcademicYearModel).filter(
                AcademicYearModel.school_id == school_id,
                AcademicYearModel.is_active == True
            ).first()
        finally:
            pass


class AcademicYearRepository(BaseRepository[AcademicYearModel]):
    """Repository for Academic Year operations"""
    
    def __init__(self):
        super().__init__(AcademicYearModel)
    
    def get_by_school(self, school_id: int) -> List[AcademicYearModel]:
        """Get all academic years for a school"""
        session = self.get_session()
        try:
            return session.query(AcademicYearModel).filter(
                AcademicYearModel.school_id == school_id
            ).all()
        finally:
            pass
    
    def get_active(self) -> Optional[AcademicYearModel]:
        """Get currently active academic year"""
        session = self.get_session()
        try:
            return session.query(AcademicYearModel).filter(
                AcademicYearModel.is_active == True
            ).first()
        finally:
            pass


class GradeRepository(BaseRepository[GradeModel]):
    """Repository for Grade operations"""
    
    def __init__(self):
        super().__init__(GradeModel)
    
    def get_by_academic_year(self, academic_year_id: int) -> List[GradeModel]:
        """Get grades by academic year"""
        session = self.get_session()
        try:
            return session.query(GradeModel).filter(
                GradeModel.academic_year_id == academic_year_id
            ).all()
        finally:
            pass
    
    def get_by_level(self, level: str) -> List[GradeModel]:
        """Get grades by level (primary/secondary)"""
        session = self.get_session()
        try:
            return session.query(GradeModel).filter(GradeModel.level == level).all()
        finally:
            pass


class CourseRepository(BaseRepository[CourseModel]):
    """Repository for Course operations"""
    
    def __init__(self):
        super().__init__(CourseModel)
    
    def get_by_grade(self, grade_id: int) -> List[CourseModel]:
        """Get courses by grade"""
        session = self.get_session()
        try:
            return session.query(CourseModel).filter(
                CourseModel.grade_id == grade_id
            ).all()
        finally:
            pass
    
    def get_by_code(self, code: str) -> Optional[CourseModel]:
        """Get course by code"""
        session = self.get_session()
        try:
            return session.query(CourseModel).filter(CourseModel.code == code).first()
        finally:
            pass


class ClassroomRepository(BaseRepository[ClassroomModel]):
    """Repository for Classroom operations"""
    
    def __init__(self):
        super().__init__(ClassroomModel)
    
    def get_available(self) -> List[ClassroomModel]:
        """Get available classrooms"""
        session = self.get_session()
        try:
            return session.query(ClassroomModel).filter(
                ClassroomModel.is_active == True
            ).all()
        finally:
            pass
    
    def get_by_number(self, number: str) -> Optional[ClassroomModel]:
        """Get classroom by number"""
        session = self.get_session()
        try:
            return session.query(ClassroomModel).filter(
                ClassroomModel.number == number
            ).first()
        finally:
            pass
