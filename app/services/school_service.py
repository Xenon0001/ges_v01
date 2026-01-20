"""
School service for GES application
Handles school-related business logic
"""

from typing import List, Optional
from app.repositories.school_repository import SchoolRepository
from app.repositories.grade_repository import GradeRepository
from app.repositories.academic_year_repository import AcademicYearRepository
from database.models.school import SchoolModel, GradeModel, AcademicYearModel


class SchoolService:
    """Service for school-related operations"""
    
    def __init__(self):
        self.school_repository = SchoolRepository()
        self.grade_repository = GradeRepository()
        self.academic_year_repository = AcademicYearRepository()
    
    # School operations
    def get_school(self) -> Optional[SchoolModel]:
        """Get the school information"""
        return self.school_repository.get_school()
    
    def create_school(self, name: str, address: str = "", phone: str = "", 
                    email: str = "", website: str = "") -> SchoolModel:
        """Create a new school"""
        return self.school_repository.create_school(name, address, phone, email, website)
    
    def update_school(self, school_id: int, name: str = None, address: str = None,
                    phone: str = None, email: str = None, website: str = None) -> Optional[SchoolModel]:
        """Update school information"""
        return self.school_repository.update_school(school_id, name, address, phone, email, website)
    
    # Grade operations
    def get_grades(self) -> List[GradeModel]:
        """Get all grades"""
        return self.grade_repository.get_all_grades()
    
    def get_grade_by_id(self, grade_id: int) -> Optional[GradeModel]:
        """Get grade by ID"""
        return self.grade_repository.get_grade_by_id(grade_id)
    
    def create_grade(self, name: str, level: int = 1) -> GradeModel:
        """Create a new grade"""
        return self.grade_repository.create_grade(name, level)
    
    def update_grade(self, grade_id: int, name: str = None, level: int = None) -> Optional[GradeModel]:
        """Update grade information"""
        return self.grade_repository.update_grade(grade_id, name, level)
    
    def delete_grade(self, grade_id: int) -> bool:
        """Delete a grade"""
        return self.grade_repository.delete_grade(grade_id)
    
    # Academic year operations
    def get_academic_years(self) -> List[AcademicYearModel]:
        """Get all academic years"""
        return self.academic_year_repository.get_all_academic_years()
    
    def get_academic_year_by_id(self, year_id: int) -> Optional[AcademicYearModel]:
        """Get academic year by ID"""
        return self.academic_year_repository.get_academic_year_by_id(year_id)
    
    def get_active_academic_year(self) -> Optional[AcademicYearModel]:
        """Get the active academic year"""
        return self.academic_year_repository.get_active_academic_year()
    
    def create_academic_year(self, name: str, start_date, end_date, is_active: bool = False) -> AcademicYearModel:
        """Create a new academic year"""
        return self.academic_year_repository.create_academic_year(name, start_date, end_date, is_active)
    
    def update_academic_year(self, year_id: int, name: str = None, start_date = None,
                           end_date = None, is_active: bool = None) -> Optional[AcademicYearModel]:
        """Update academic year information"""
        return self.academic_year_repository.update_academic_year(year_id, name, start_date, end_date, is_active)
    
    def delete_academic_year(self, year_id: int) -> bool:
        """Delete an academic year"""
        return self.academic_year_repository.delete_academic_year(year_id)
    
    def set_active_academic_year(self, year_id: int) -> Optional[AcademicYearModel]:
        """Set an academic year as active (deactivates others)"""
        return self.academic_year_repository.set_active_academic_year(year_id)
