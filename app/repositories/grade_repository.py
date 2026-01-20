"""
Grade repository for GES application
Handles grade data operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.school import GradeModel
from database.db import get_db_session


class GradeRepository:
    """Repository for grade operations"""
    
    def __init__(self):
        self.session_factory = get_db_session
    
    def get_all_grades(self) -> List[GradeModel]:
        """Get all grades"""
        with self.session_factory() as session:
            return session.query(GradeModel).order_by(GradeModel.level).all()
    
    def get_grade_by_id(self, grade_id: int) -> Optional[GradeModel]:
        """Get grade by ID"""
        with self.session_factory() as session:
            return session.query(GradeModel).filter(GradeModel.id == grade_id).first()
    
    def get_grade_by_name(self, name: str) -> Optional[GradeModel]:
        """Get grade by name"""
        with self.session_factory() as session:
            return session.query(GradeModel).filter(GradeModel.name == name).first()
    
    def create_grade(self, name: str, level: int = 1) -> GradeModel:
        """Create a new grade"""
        with self.session_factory() as session:
            # Check if grade already exists
            existing = session.query(GradeModel).filter(GradeModel.name == name).first()
            if existing:
                return existing
            
            grade = GradeModel(name=name, level=level)
            session.add(grade)
            session.commit()
            session.refresh(grade)
            return grade
    
    def update_grade(self, grade_id: int, name: str = None, level: int = None) -> Optional[GradeModel]:
        """Update grade information"""
        with self.session_factory() as session:
            grade = session.query(GradeModel).filter(GradeModel.id == grade_id).first()
            if not grade:
                return None
            
            if name is not None:
                grade.name = name
            if level is not None:
                grade.level = level
            
            session.commit()
            session.refresh(grade)
            return grade
    
    def delete_grade(self, grade_id: int) -> bool:
        """Delete a grade"""
        with self.session_factory() as session:
            grade = session.query(GradeModel).filter(GradeModel.id == grade_id).first()
            if not grade:
                return False
            
            session.delete(grade)
            session.commit()
            return True
