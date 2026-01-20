"""
Tutor service for GES application
Handles tutor management operations
"""

from typing import List, Optional
from datetime import date, datetime
from app.repositories.student_repository import TutorRepository
from app.repositories.user_repository import PersonRepository
from database.models.person import TutorModel, PersonModel
from app.domain.entities import Tutor


class TutorService:
    """Service for tutor management operations"""
    
    def __init__(self):
        self.tutor_repo = TutorRepository()
        self.person_repo = PersonRepository()
    
    def create_tutor(self, tutor_data: dict) -> TutorModel:
        """Create new tutor with validation"""
        
        # Validate required fields
        required_fields = ['name', 'last_name']
        for field in required_fields:
            if not tutor_data.get(field):
                raise ValueError(f"Field '{field}' is required")
        
        # Create person record
        person = PersonModel(
            name=tutor_data['name'],
            last_name=tutor_data['last_name'],
            email=tutor_data.get('email'),
            phone=tutor_data.get('phone'),
            address=tutor_data.get('address'),
            birth_date=tutor_data.get('birth_date')
        )
        
        # Create tutor record
        tutor = TutorModel(
            occupation=tutor_data.get('occupation'),
            workplace=tutor_data.get('workplace'),
            relationship=tutor_data.get('relationship', 'Parent'),
            emergency_contact=tutor_data.get('emergency_contact', False),
            person_id=person.id
        )
        
        return self.tutor_repo.create(tutor)
    
    def get_tutor_by_id(self, tutor_id: int) -> Optional[TutorModel]:
        """Get tutor by database ID"""
        return self.tutor_repo.get_by_id(tutor_id)
    
    def get_all_tutors(self) -> List[TutorModel]:
        """Get all tutors"""
        return self.tutor_repo.get_all()
    
    def search_tutors(self, name: str = None) -> List[TutorModel]:
        """Search tutors by name"""
        return self.tutor_repo.search(name)
    
    def update_tutor(self, tutor_id: int, update_data: dict) -> TutorModel:
        """Update tutor information"""
        tutor = self.tutor_repo.get_by_id(tutor_id)
        if not tutor:
            raise ValueError("Tutor not found")
        
        # Update fields
        for field, value in update_data.items():
            if hasattr(tutor, field) and value is not None:
                setattr(tutor, field, value)
        
        return self.tutor_repo.update(tutor)
    
    def delete_tutor(self, tutor_id: int) -> bool:
        """Delete tutor"""
        try:
            return self.tutor_repo.delete(tutor_id)
        except Exception:
            return False
    
    def get_tutor_students(self, tutor_id: int) -> List:
        """Get students associated with tutor"""
        # This would need to be implemented in repositories
        # For now, return empty list
        return []
