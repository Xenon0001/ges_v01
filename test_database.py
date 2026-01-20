#!/usr/bin/env python3
"""
Test script for GES database setup
Creates database, tables, and sample data
"""

import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_database, get_db
from database.models import SchoolModel, StudentModel, EnrollmentModel, PaymentModel


def test_database_creation():
    """Test database and table creation"""
    print("🧪 Testing database creation...")
    
    # Initialize database
    if not init_database():
        print("❌ Database initialization failed")
        return False
    
    print("✅ Database creation test passed")
    return True


def test_basic_operations():
    """Test basic CRUD operations"""
    print("🧪 Testing basic operations...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Test query
        schools = db.query(SchoolModel).all()
        print(f"📊 Found {len(schools)} schools")
        
        if schools:
            school = schools[0]
            print(f"🏫 School: {school.name}")
            print(f"📅 Academic Year: {school.academic_year}")
        
        # Test student query
        students = db.query(StudentModel).all()
        print(f"👨‍🎓 Found {len(students)} students")
        
        # Test enrollment query
        enrollments = db.query(EnrollmentModel).all()
        print(f"📝 Found {len(enrollments)} enrollments")
        
        # Test payment query
        payments = db.query(PaymentModel).all()
        print(f"💰 Found {len(payments)} payments")
        
        db.close()
        print("✅ Basic operations test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic operations test failed: {e}")
        return False


def test_entity_creation():
    """Test creating new entities"""
    print("🧪 Testing entity creation...")
    
    try:
        db = next(get_db())
        
        # Create a new student
        from database.models import PersonModel, StudentModel, TutorModel
        
        person = PersonModel(
            name="Test",
            last_name="Student",
            email="test@student.com",
            phone="+240 123 456"
        )
        db.add(person)
        db.flush()
        
        student = StudentModel(
            student_id=f"EST{2024}001",
            enrollment_date=datetime.now().date(),
            person_id=person.id
        )
        db.add(student)
        
        db.commit()
        print("✅ Created test student successfully")
        
        # Clean up
        db.delete(student)
        db.delete(person)
        db.commit()
        
        db.close()
        print("✅ Entity creation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Entity creation test failed: {e}")
        return False


def main():
    """Run all database tests"""
    print("🚀 Starting GES Database Tests")
    print("=" * 50)
    
    tests = [
        test_database_creation,
        test_basic_operations,
        test_entity_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 50)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Database is ready for use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
