"""
Sidebar component for GES application
Navigation menu for main window
"""

import customtkinter as ctk
from typing import Callable, Optional


class Sidebar:
    """Sidebar navigation component"""
    
    def __init__(self, parent, on_menu_select: Optional[Callable] = None):
        self.parent = parent
        self.on_menu_select = on_menu_select
        self.current_menu = "home"
        self.menu_buttons = {}
        self._initializing = True  # Flag para evitar callbacks durante init
        
        self.create_widgets()
        self._initializing = False  # Permitir callbacks después de init
    
    def create_widgets(self):
        """Create sidebar widgets"""
        # Sidebar frame - NO usar pack aquí
        self.frame = ctk.CTkFrame(self.parent, width=250, corner_radius=0)
        # NO usar pack() - dejar que el padre lo maneje con grid()
        
        # Logo/Title area
        title_frame = ctk.CTkFrame(self.frame)
        title_frame.pack(pady=20, padx=10, fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="GES",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Gestión Escolar",
            font=ctk.CTkFont(size=12)
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Navigation menu
        self.create_menu_items()
        
        # Logout button at bottom
        logout_frame = ctk.CTkFrame(self.frame)
        logout_frame.pack(side="bottom", pady=20, padx=10, fill="x")
        
        self.logout_button = ctk.CTkButton(
            logout_frame,
            text="Cerrar Sesión",
            command=self.handle_logout,
            fg_color="red",
            hover_color="darkred"
        )
        self.logout_button.pack(pady=10, padx=10, fill="x")
    
    def create_menu_items(self):
        """Create navigation menu items"""
        menu_items = [
            ("home", "Inicio", "🏠"),
            ("students", "Estudiantes", "👥"),
            ("enrollments", "Matrículas", "📝"),
            ("reports", "Reportes", "📊"),
            ("settings", "Ajustes", "⚙️")
        ]
        
        for menu_id, text, icon in menu_items:
            # Create menu button
            button = ctk.CTkButton(
                self.frame,
                text=f"{icon} {text}",
                command=lambda mid=menu_id: self.select_menu(mid),
                height=40,
                corner_radius=0,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w"
            )
            button.pack(pady=2, padx=10, fill="x")
            
            self.menu_buttons[menu_id] = button
        
        # Seleccionar "home" por defecto pero SIN disparar el callback
        # Solo actualizar el estilo visual
        if "home" in self.menu_buttons:
            self.menu_buttons["home"].configure(
                fg_color=("gray75", "gray25"),
                text_color=("gray10", "gray90")
            )
    
    def select_menu(self, menu_id: str):
        """Handle menu selection"""
        # Update button styles
        for mid, button in self.menu_buttons.items():
            if mid == menu_id:
                # Highlight selected menu
                button.configure(
                    fg_color=("gray75", "gray25"),
                    text_color=("gray10", "gray90")
                )
            else:
                # Reset other buttons
                button.configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90")
                )
        
        self.current_menu = menu_id
        
        # Solo llamar callback si NO estamos inicializando
        if self._initializing:
            return
        
        # Call callback if provided
        if self.on_menu_select:
            # Map menu items to view classes
            from app.ui.students.students_view import StudentsView
            from app.ui.enrollments.enrollments_view import EnrollmentsView
            from app.ui.reports_view import ReportsView
            from app.ui.settings_view import SettingsView
            
            menu_items = {
                "home": ("home", None),
                "students": ("students", StudentsView),
                "enrollments": ("enrollments", EnrollmentsView),
                "reports": ("reports", ReportsView),
                "settings": ("settings", SettingsView)
            }
            
            if menu_id in menu_items:
                view_name, view_class = menu_items[menu_id]
                self.on_menu_select(view_name, view_class)
    
    def handle_logout(self):
        """Handle logout button click"""
        # Call callback if provided
        if self.on_menu_select:
            self.on_menu_select("logout", None)
    
    def set_menu_callback(self, callback: Callable):
        """Set menu selection callback"""
        self.on_menu_select = callback
    
    def get_current_menu(self) -> str:
        """Get currently selected menu"""
        return self.current_menu
    
    def highlight_menu(self, menu_id: str):
        """Programmatically highlight a menu item"""
        self.select_menu(menu_id)