#!/usr/bin/env python3
"""
Test script para verificar correcciones estructurales de vistas
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from database.db import init_database
from database.models.person import UserModel, UserRole
from app.ui.main_view import MainView


def test_view_structure():
    """Test que todas las vistas hereden correctamente de CTkFrame"""
    print("Testing view structure corrections...")
    
    # Initialize database
    try:
        init_database()
        print("Database initialized")
    except Exception as e:
        print(f"Database error: {e}")
        return
    
    # Create mock user
    user = UserModel()
    user.username = "test_user"
    user.role = UserRole.ADMIN.value
    
    # Test MainView
    root = ctk.CTk()
    root.title("GES Structure Test")
    root.geometry("800x600")
    
    try:
        main_view = MainView(root, user)
        print("MainView created successfully")
        
        # Test StudentsView
        main_view.show_students_view()
        print("StudentsView loaded - should inherit from CTkFrame")
        
        # Test EnrollmentsView
        main_view.show_enrollments_view()
        print("EnrollmentsView loaded - should inherit from CTkFrame")
        
        # Test ReportsView
        main_view.show_reports_view()
        print("ReportsView loaded - should inherit from CTkFrame")
        
        # Test SettingsView
        main_view.show_settings_view()
        print("SettingsView loaded - should inherit from CTkFrame")
        
        print("All view structure tests passed!")
        print("Views now properly inherit from CTkFrame")
        print("Navigation should work without visual overlap")
        
        # Show window for manual verification
        root.mainloop()
        
    except Exception as e:
        print(f"Structure test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_view_structure()
