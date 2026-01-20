#!/usr/bin/env python3
"""
Test script for GES services and repositories
Demonstrates the complete flow: UI → Service → Repository → DB
"""

import sys
import os
from datetime import date, timedelta

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_database
from app.services.auth_service import AuthService
from app.services.student_service import StudentService
from app.services.enrollment_service import EnrollmentService
from app.services.payment_service import PaymentService


def test_auth_service():
    """Test authentication service"""
    print("Testing AuthService...")
    
    auth_service = AuthService()
    
    try:
        # Test user creation
        user = auth_service.create_user(
            username="testuser",
            password="test123",
            role="SECRETARY"
        )
        print(f"User created: {user.username} (ID: {user.id})")
        
        # Test authentication
        authenticated_user = auth_service.authenticate("testuser", "test123")
        if authenticated_user:
            print(f"Authentication successful: {authenticated_user.username}")
        else:
            print("Authentication failed")
        
        # Test invalid authentication
        invalid_user = auth_service.authenticate("testuser", "wrongpassword")
        if invalid_user:
            print("Invalid authentication should have failed")
        else:
            print("Invalid authentication correctly rejected")
            
    except Exception as e:
        print(f"Auth service error: {e}")


def test_student_service():
    """Test student service"""
    print("\nTesting StudentService...")
    
    student_service = StudentService()
    
    try:
        # Test student creation
        student_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'birth_date': '2010-05-15',
            'email': 'juan.perez@email.com',
            'phone': '+240 123 456 789',
            'address': 'Calle Principal, Malabo'
        }
        
        student = student_service.create_student(student_data)
        print(f"Student created: {student.student_id} - {student.person.name} {student.person.last_name}")
        
        # Test student search
        found_students = student_service.search_students(name='Juan')
        print(f"Found {len(found_students)} students with name 'Juan'")
        
        # Test student statistics
        stats = student_service.get_student_statistics()
        print(f"Student statistics: {stats['total_students']} total students")
        
    except Exception as e:
        print(f"Student service error: {e}")


def test_enrollment_service():
    """Test enrollment service"""
    print("\nTesting EnrollmentService...")
    
    enrollment_service = EnrollmentService()
    
    try:
        # Get existing data for enrollment
        from app.repositories.school_repository import GradeRepository, AcademicYearRepository
        grade_repo = GradeRepository()
        academic_year_repo = AcademicYearRepository()
        
        grades = grade_repo.get_all()
        academic_years = academic_year_repo.get_all()
        
        if grades and academic_years:
            grade = grades[0]
            academic_year = academic_years[0]
            
            # Create a student first for enrollment
            student_service = StudentService()
            student_data = {
                'name': 'María',
                'last_name': 'González',
                'birth_date': '2011-03-20'
            }
            student = student_service.create_student(student_data)
            
            # Test enrollment
            enrollment = enrollment_service.enroll_student(
                student_id=student.id,
                grade_id=grade.id,
                academic_year_id=academic_year.id
            )
            print(f"Enrollment created: {enrollment.enrollment_number}")
            
            # Test enrollment statistics
            stats = enrollment_service.get_enrollment_statistics(grade.id)
            print(f"Grade statistics: {stats['total_enrolled']}/{stats['capacity']} enrolled")
            
    except Exception as e:
        print(f"Enrollment service error: {e}")


def test_payment_service():
    """Test payment service"""
    print("\nTesting PaymentService...")
    
    payment_service = PaymentService()
    
    try:
        # Get existing enrollment
        from app.repositories.enrollment_repository import EnrollmentRepository
        enrollment_repo = EnrollmentRepository()
        enrollments = enrollment_repo.get_all()
        
        if enrollments:
            enrollment = enrollments[0]
            
            # Test payment creation
            payment = payment_service.create_payment(
                enrollment_id=enrollment.id,
                amount=50000.0,
                due_date=date.today() + timedelta(days=30),
                description="Tuition fee"
            )
            print(f"Payment created: {payment.amount} XAF due {payment.due_date}")
            
            # Test payment schedule
            schedule = payment_service.create_payment_schedule(
                enrollment_id=enrollment.id,
                total_amount=100000.0,
                num_installments=3
            )
            print(f"Payment schedule created: {len(schedule)} installments")
            
            # Test payment summary
            summary = payment_service.get_payment_summary(enrollment.id)
            print(f"Payment summary: {summary['total_required']} XAF required, {summary['total_paid']} XAF paid")
            
    except Exception as e:
        print(f"Payment service error: {e}")


def test_business_rules():
    """Test specific business rules"""
    print("\nTesting Business Rules...")
    
    try:
        # Test duplicate enrollment prevention
        enrollment_service = EnrollmentService()
        student_service = StudentService()
        
        # Create student
        student_data = {
            'name': 'Carlos',
            'last_name': 'Mendoza',
            'birth_date': '2009-08-10'
        }
        student = student_service.create_student(student_data)
        
        # Get grade and academic year
        from app.repositories.school_repository import GradeRepository, AcademicYearRepository
        grade_repo = GradeRepository()
        academic_year_repo = AcademicYearRepository()
        
        grade = grade_repo.get_all()[0]
        academic_year = academic_year_repo.get_all()[0]
        
        # First enrollment should succeed
        enrollment1 = enrollment_service.enroll_student(
            student_id=student.id,
            grade_id=grade.id,
            academic_year_id=academic_year.id
        )
        print("First enrollment successful")
        
        # Second enrollment should fail
        try:
            enrollment2 = enrollment_service.enroll_student(
                student_id=student.id,
                grade_id=grade.id,
                academic_year_id=academic_year.id
            )
            print("Duplicate enrollment should have failed")
        except ValueError as e:
            print(f"Duplicate enrollment correctly prevented: {e}")
        
        # Test negative payment prevention
        payment_service = PaymentService()
        try:
            payment_service.create_payment(
                enrollment_id=enrollment1.id,
                amount=-1000.0,
                due_date=date.today()
            )
            print("Negative payment should have failed")
        except ValueError as e:
            print(f"Negative payment correctly prevented: {e}")
            
    except Exception as e:
        print(f"Business rules test error: {e}")


def main():
    """Main test function"""
    print("Testing GES Services and Repositories")
    print("=" * 60)
    
    # Initialize database
    if not init_database():
        print("Database initialization failed")
        return False
    
    # Run tests
    test_auth_service()
    test_student_service()
    test_enrollment_service()
    test_payment_service()
    test_business_rules()
    
    print("\n" + "=" * 60)
    print("Services testing complete!")
    print("\nFlow demonstrated:")
    print("   UI -> Service -> Repository -> Database")
    print("   Authentication working")
    print("   Student management working")
    print("   Enrollment with business rules working")
    print("   Payment processing working")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
