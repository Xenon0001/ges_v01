#!/usr/bin/env python3
"""
GES - Sistema de Gestión Escolar
Main application entry point
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_database
from app.ui.login_view import LoginView
from app.ui.main_view import MainApplication


def initialize_database():
    """Initialize database with default data"""
    try:
        init_database()
        print("Base de datos inicializada correctamente")
        return True
            
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False


def main():
    """Main application entry point"""
    print("Iniciando GES - Sistema de Gestión Escolar...")
    
    # Initialize database
    if not initialize_database():
        print("No se pudo inicializar la base de datos. Saliendo...")
        return
    
    def on_login_success(user):
        """Handle successful login"""
        # Create and show main application
        main_app = MainApplication(user)
        main_app.show()
        
    # Show login window
    login_view = LoginView()
    login_view.show(on_login_success)


if __name__ == "__main__":
    main()
