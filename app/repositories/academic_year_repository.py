"""
Academic year repository for GES application
Handles academic year data operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.school import AcademicYearModel
from database.db import get_db_session


class AcademicYearRepository:
    """Repository for academic year operations"""
    
    def __init__(self):
        self.session_factory = get_db_session
    
    def get_all_academic_years(self) -> List[AcademicYearModel]:
        """Get all academic years"""
        with self.session_factory() as session:
            return session.query(AcademicYearModel).order_by(AcademicYearModel.start_date.desc()).all()
    
    def get_academic_year_by_id(self, year_id: int) -> Optional[AcademicYearModel]:
        """Get academic year by ID"""
        with self.session_factory() as session:
            return session.query(AcademicYearModel).filter(AcademicYearModel.id == year_id).first()
    
    def get_academic_year_by_name(self, name: str) -> Optional[AcademicYearModel]:
        """Get academic year by name"""
        with self.session_factory() as session:
            return session.query(AcademicYearModel).filter(AcademicYearModel.name == name).first()
    
    def get_active_academic_year(self) -> Optional[AcademicYearModel]:
        """Get the active academic year"""
        with self.session_factory() as session:
            return session.query(AcademicYearModel).filter(AcademicYearModel.is_active == True).first()
    
    def create_academic_year(self, name: str, start_date, end_date, is_active: bool = False) -> AcademicYearModel:
        """Create a new academic year"""
        with self.session_factory() as session:
            # If this is active, deactivate all others
            if is_active:
                session.query(AcademicYearModel).filter(AcademicYearModel.is_active == True).update(
                    {"is_active": False}, synchronize_session=False
                )
            
            academic_year = AcademicYearModel(
                name=name,
                start_date=start_date,
                end_date=end_date,
                is_active=is_active
            )
            session.add(academic_year)
            session.commit()
            session.refresh(academic_year)
            return academic_year
    
    def update_academic_year(self, year_id: int, name: str = None, start_date = None,
                           end_date = None, is_active: bool = None) -> Optional[AcademicYearModel]:
        """Update academic year information"""
        with self.session_factory() as session:
            academic_year = session.query(AcademicYearModel).filter(AcademicYearModel.id == year_id).first()
            if not academic_year:
                return None
            
            # If setting as active, deactivate all others
            if is_active is True and not academic_year.is_active:
                session.query(AcademicYearModel).filter(AcademicYearModel.is_active == True).update(
                    {"is_active": False}, synchronize_session=False
                )
            
            if name is not None:
                academic_year.name = name
            if start_date is not None:
                academic_year.start_date = start_date
            if end_date is not None:
                academic_year.end_date = end_date
            if is_active is not None:
                academic_year.is_active = is_active
            
            session.commit()
            session.refresh(academic_year)
            return academic_year
    
    def delete_academic_year(self, year_id: int) -> bool:
        """Delete an academic year"""
        with self.session_factory() as session:
            academic_year = session.query(AcademicYearModel).filter(AcademicYearModel.id == year_id).first()
            if not academic_year:
                return False
            
            session.delete(academic_year)
            session.commit()
            return True
    
    def set_active_academic_year(self, year_id: int) -> Optional[AcademicYearModel]:
        """Set an academic year as active (deactivates others)"""
        with self.session_factory() as session:
            # Deactivate all academic years
            session.query(AcademicYearModel).filter(AcademicYearModel.is_active == True).update(
                {"is_active": False}, synchronize_session=False
            )
            
            # Activate the specified one
            academic_year = session.query(AcademicYearModel).filter(AcademicYearModel.id == year_id).first()
            if academic_year:
                academic_year.is_active = True
                session.commit()
                session.refresh(academic_year)
            
            return academic_year
