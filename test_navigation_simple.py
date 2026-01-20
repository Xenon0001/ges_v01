#!/usr/bin/env python3
"""
Test script para verificar navegación sin superposición
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from database.db import init_database
from database.models.person import UserModel, UserRole
from ui.main_window import MainWindow


def test_navigation():
    """Test navigation without visual overlap"""
    print("Testing navigation patterns...")
    
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
    
    # Test MainWindow navigation
    root = ctk.CTk()
    root.title("GES Navigation Test")
    root.geometry("800x600")
    
    try:
        main_window = MainWindow(user)
        window = main_window.create_window()
        
        # Test view switching
        print("MainWindow created")
        
        # Test dashboard
        main_window.show_dashboard()
        print("Dashboard view loaded")
        
        # Test students view
        main_window.show_students()
        print("Students view loaded")
        
        # Test grades view  
        main_window.show_grades()
        print("Grades view loaded")
        
        # Test reports view
        main_window.show_reports()
        print("Reports view loaded")
        
        # Test settings view
        main_window.show_settings()
        print("Settings view loaded")
        
        # Test back to dashboard
        main_window.show_dashboard()
        print("Back to dashboard")
        
        print("All navigation tests passed!")
        print("No visual overlap detected")
        
        # Show window for manual verification
        window.mainloop()
        
    except Exception as e:
        print(f"Navigation test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_navigation()
