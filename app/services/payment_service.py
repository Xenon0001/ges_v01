"""
Payment service for GES application
Handles payment processing and business rules
"""

from typing import List, Optional
from datetime import date, timedelta
from app.repositories.enrollment_repository import PaymentRepository, EnrollmentRepository
from app.repositories.school_repository import AcademicYearRepository
from database.models.enrollment import PaymentModel, EnrollmentModel
from database.models.school import AcademicYearModel
from app.domain.entities import Payment


class PaymentService:
    """Service for payment operations and business rules"""
    
    def __init__(self):
        self.payment_repo = PaymentRepository()
        self.enrollment_repo = EnrollmentRepository()
        self.academic_year_repo = AcademicYearRepository()
    
    def create_payment(self, enrollment_id: int, amount: float, due_date: date, 
                     description: str = "", academic_year_id: int = None) -> PaymentModel:
        """Create payment with business validation"""
        
        # Validate inputs
        if not enrollment_id or amount <= 0 or not due_date:
            raise ValueError("Enrollment ID, positive amount, and due date are required")
        
        # BUSINESS RULE: No negative payments
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        
        # Get enrollment to validate
        enrollment = self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise ValueError("Enrollment not found")
        
        # Get academic year for payment
        if academic_year_id:
            academic_year = self.academic_year_repo.get_by_id(academic_year_id)
        else:
            academic_year = self.enrollment_repo.get_by_academic_year(enrollment.academic_year_id)
        
        # Create payment
        payment = PaymentModel(
            enrollment_id=enrollment_id,
            amount=amount,
            due_date=due_date,
            description=description,
            academic_year_id=academic_year_id or enrollment.academic_year_id
        )
        
        return self.payment_repo.create(payment)
    
    def create_payment_schedule(self, enrollment_id: int, total_amount: float, 
                           num_installments: int = 1) -> List[PaymentModel]:
        """Create payment schedule for enrollment"""
        
        if total_amount <= 0 or num_installments <= 0:
            raise ValueError("Total amount and number of installments must be positive")
        
        installment_amount = total_amount / num_installments
        payments = []
        
        # Create installments monthly
        for i in range(num_installments):
            due_date = date.today() + timedelta(days=30 * (i + 1))
            description = f"Installment {i + 1} of {num_installments}"
            
            payment = self.create_payment(
                enrollment_id=enrollment_id,
                amount=installment_amount,
                due_date=due_date,
                description=description
            )
            payments.append(payment)
        
        return payments
    
    def process_payment(self, payment_id: int, amount_paid: float, 
                     payment_method: str = None) -> bool:
        """Process payment with validation"""
        from database.models.enrollment import PaymentStatus
        
        # Get payment
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        
        # Validate payment amount
        if amount_paid <= 0:
            raise ValueError("Payment amount must be positive")
        
        # Check if payment is already paid
        if payment.status == PaymentStatus.PAID.value:
            raise ValueError("Payment is already processed")
        
        # Update payment status
        if amount_paid >= payment.amount:
            # Full payment
            self.payment_repo.update_status(payment_id, PaymentStatus.PAID.value, payment_method)
            return True
        else:
            # Partial payment (could implement partial payment logic)
            raise ValueError("Partial payments not supported yet")
    
    def get_overdue_payments(self) -> List[PaymentModel]:
        """Get all overdue payments"""
        return self.payment_repo.get_overdue()
    
    def get_pending_payments(self, enrollment_id: int = None) -> List[PaymentModel]:
        """Get pending payments"""
        return self.payment_repo.get_pending(enrollment_id)
    
    def get_payment_summary(self, enrollment_id: int) -> dict:
        """Get payment summary for enrollment"""
        payments = self.payment_repo.get_by_enrollment(enrollment_id)
        total_paid = self.payment_repo.get_total_paid(enrollment_id)
        
        total_required = sum(p.amount for p in payments)
        pending_amount = total_required - total_paid
        
        return {
            'total_required': total_required,
            'total_paid': total_paid,
            'pending_amount': pending_amount,
            'payment_status': 'paid' if pending_amount <= 0 else 'pending',
            'total_payments': len(payments),
            'paid_payments': len([p for p in payments if p.status == 'paid']),
            'pending_payments': len([p for p in payments if p.status == 'pending'])
        }
    
    def send_payment_reminders(self) -> List[PaymentModel]:
        """Get payments that need reminders (due soon)"""
        pending_payments = self.payment_repo.get_pending()
        
        # Payments due in next 7 days
        reminder_date = date.today() + timedelta(days=7)
        
        return [
            payment for payment in pending_payments 
            if payment.due_date <= reminder_date
        ]
    
    def calculate_late_fee(self, payment_id: int, daily_rate: float = 0.01) -> float:
        """Calculate late fee for overdue payment"""
        
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment or payment.status != 'pending':
            return 0.0
        
        days_overdue = (date.today() - payment.due_date).days
        if days_overdue <= 0:
            return 0.0
        
        return payment.amount * daily_rate * days_overdue
    
    def get_tutor_payment_summary(self, tutor_id: int) -> dict:
        """Get payment summary for all students under a tutor"""
        enrollments = self.enrollment_repo.get_by_tutor(tutor_id)
        
        total_required = 0.0
        total_paid = 0.0
        
        for enrollment in enrollments:
            summary = self.get_payment_summary(enrollment.id)
            total_required += summary['total_required']
            total_paid += summary['total_paid']
        
        return {
            'tutor_id': tutor_id,
            'total_students': len(enrollments),
            'total_required': total_required,
            'total_paid': total_paid,
            'total_pending': total_required - total_paid,
            'payment_rate': (total_paid / total_required * 100) if total_required > 0 else 0
        }
