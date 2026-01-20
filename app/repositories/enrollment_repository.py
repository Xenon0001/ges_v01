"""
Enrollment repository for GES application
Handles enrollment and payment data operations
"""

from typing import List, Optional
from database.models.enrollment import EnrollmentModel, PaymentModel
from database.models.school import GradeModel
from .base_repository import BaseRepository


class EnrollmentRepository(BaseRepository[EnrollmentModel]):
    """Repository for Enrollment operations"""
    
    def __init__(self):
        super().__init__(EnrollmentModel)
    
    def get_by_enrollment_number(self, enrollment_number: str) -> Optional[EnrollmentModel]:
        """Get enrollment by enrollment number"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.enrollment_number == enrollment_number
            ).first()
        finally:
            pass
    
    def get_by_student_and_year(self, student_id: int, academic_year_id: int) -> Optional[EnrollmentModel]:
        """Get student's enrollment for specific academic year"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.student_id == student_id,
                EnrollmentModel.academic_year_id == academic_year_id
            ).first()
        finally:
            pass
    
    def get_by_grade(self, grade_id: int) -> List[EnrollmentModel]:
        """Get all enrollments for a grade"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.grade_id == grade_id,
                EnrollmentModel.status == 'active'
            ).all()
        finally:
            pass
    
    def get_by_tutor(self, tutor_id: int) -> List[EnrollmentModel]:
        """Get all enrollments for a tutor"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.tutor_id == tutor_id,
                EnrollmentModel.status == 'active'
            ).all()
        finally:
            pass
    
    def get_by_academic_year(self, academic_year_id: int) -> List[EnrollmentModel]:
        """Get all enrollments for an academic year"""
        session = self.get_session()
        try:
            return session.query(EnrollmentModel).filter(
                EnrollmentModel.academic_year_id == academic_year_id
            ).all()
        finally:
            pass
    
    def update_status(self, enrollment_id: int, status: str):
        """Update enrollment status"""
        session = self.get_session()
        try:
            enrollment = session.query(EnrollmentModel).filter(
                EnrollmentModel.id == enrollment_id
            ).first()
            if enrollment:
                enrollment.status = status
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            pass


class PaymentRepository(BaseRepository[PaymentModel]):
    """Repository for Payment operations"""
    
    def __init__(self):
        super().__init__(PaymentModel)
    
    def get_by_enrollment(self, enrollment_id: int) -> List[PaymentModel]:
        """Get all payments for an enrollment"""
        session = self.get_session()
        try:
            return session.query(PaymentModel).filter(
                PaymentModel.enrollment_id == enrollment_id
            ).all()
        finally:
            pass
    
    def get_overdue(self) -> List[PaymentModel]:
        """Get all overdue payments"""
        session = self.get_session()
        try:
            from database.models.enrollment import PaymentStatus
            from datetime import date
            return session.query(PaymentModel).filter(
                PaymentModel.status == PaymentStatus.PENDING.value,
                PaymentModel.due_date < date.today()
            ).all()
        finally:
            pass
    
    def get_pending(self, enrollment_id: int = None) -> List[PaymentModel]:
        """Get pending payments"""
        session = self.get_session()
        try:
            from database.models.enrollment import PaymentStatus
            query = session.query(PaymentModel).filter(
                PaymentModel.status == PaymentStatus.PENDING.value
            )
            
            if enrollment_id:
                query = query.filter(PaymentModel.enrollment_id == enrollment_id)
            
            return query.all()
        finally:
            pass
    
    def update_status(self, payment_id: int, status: str, payment_method: str = None):
        """Update payment status"""
        session = self.get_session()
        try:
            payment = session.query(PaymentModel).filter(
                PaymentModel.id == payment_id
            ).first()
            if payment:
                payment.status = status
                if payment_method:
                    payment.payment_method = payment_method
                if status == 'PAID':
                    from datetime import date
                    payment.payment_date = date.today()
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            pass
    
    def get_total_paid(self, enrollment_id: int) -> float:
        """Get total amount paid for enrollment"""
        session = self.get_session()
        try:
            from database.models.enrollment import PaymentStatus
            result = session.query(PaymentModel).filter(
                PaymentModel.enrollment_id == enrollment_id,
                PaymentModel.status == PaymentStatus.PAID.value
            ).with_entities(
                session.query(PaymentModel.amount).label('total')
            ).scalar()
            return result or 0.0
        finally:
            pass
