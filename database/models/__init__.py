"""
Database models package for GES
"""

# Import all models to ensure they are available
from .school import (
    SchoolModel,
    AcademicYearModel,
    GradeModel,
    CourseModel,
    ClassroomModel
)

from .person import (
    PersonModel,
    UserModel,
    StudentModel,
    TutorModel,
    UserRole
)

from .enrollment import (
    EnrollmentModel,
    PaymentModel,
    EnrollmentStatus,
    PaymentStatus
)

__all__ = [
    # School models
    "SchoolModel",
    "AcademicYearModel", 
    "GradeModel",
    "CourseModel",
    "ClassroomModel",
    
    # Person models
    "PersonModel",
    "UserModel",
    "StudentModel", 
    "TutorModel",
    "UserRole",
    
    # Enrollment models
    "EnrollmentModel",
    "PaymentModel",
    "EnrollmentStatus",
    "PaymentStatus"
]