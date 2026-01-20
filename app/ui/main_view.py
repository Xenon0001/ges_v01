"""
Main view for GES application
Main window with sidebar and content area
"""

import customtkinter as ctk
from tkinter import messagebox
from app.ui.sidebar import Sidebar
from app.ui.students.students_view import StudentsView
from app.ui.enrollments.enrollments_view import EnrollmentsView
from app.ui.reports_view import ReportsView
from app.ui.settings_view import SettingsView
from database.models.person import UserModel


class MainView(ctk.CTkFrame):
    """Main application window"""
    
    def __init__(self, master, current_user: UserModel):
        super().__init__(master)
        
        self.current_user = current_user
        self.current_view = None
        self.current_view_name = None
        self.views = {}  # Cache de vistas
        self.navigation_history = []  # Historial de navegación
        
        self.pack(fill="both", expand=True)
        
        # Layout principal
        self._build_layout()
    
    def _build_layout(self):
        """Build main layout"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar (SIEMPRE VIVA)
        self.sidebar = Sidebar(self, on_menu_select=self.show_view)
        self.sidebar.frame.grid(row=0, column=0, sticky="ns")
        
        # Contenedor central (aquí van las vistas)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def show_view(self, view_name: str, view_class):
        """
        Muestra una vista en el área central.
        Nunca destruye vistas, solo las oculta.
        """
        
        # Handle special cases
        if view_name == "home":
            self.show_home_view()
            return
        
        # Guardar historial
        if self.current_view_name and self.current_view_name != view_name:
            self.navigation_history.append(self.current_view_name)
        
        # Ocultar vista actual
        if self.current_view:
            self.current_view.grid_forget()
        
        # Crear vista si no existe
        if view_name not in self.views:
            view = view_class(self.content_frame)
            view.grid(row=0, column=0, sticky="nsew")
            self.views[view_name] = view
        
        # Mostrar vista
        self.current_view = self.views[view_name]
        self.current_view_name = view_name
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_sub_view(self, sub_view_name: str, sub_view_creator):
        """Mostrar sub-vista dentro de la vista actual"""
        # Ocultar vista actual principal
        if self.current_view:
            self.current_view.grid_forget()
        
        # Cache de sub-vistas
        if sub_view_name not in self.views:
            sub_view = sub_view_creator()
            sub_view.grid(row=0, column=0, sticky="nsew")
            self.views[sub_view_name] = sub_view
        
        self.current_view = self.views[sub_view_name]
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def go_back(self):
        """Volver a vista anterior"""
        if self.navigation_history:
            prev_view_name = self.navigation_history.pop()
            # Buscar la clase de vista correspondiente
            view_classes = {
                "students": StudentsView,
                "enrollments": EnrollmentsView,
                "reports": ReportsView,
                "settings": SettingsView
            }
            
            if prev_view_name in view_classes:
                self.show_view(prev_view_name, view_classes[prev_view_name])
            else:
                self.show_home_view()
    
    def show_home_view(self):
        """Show home dashboard"""
        # Crear vista home si no existe
        if "home" not in self.views:
            home_frame = ctk.CTkFrame(self.content_frame)
            home_frame.grid(row=0, column=0, sticky="nsew")
            
            # Welcome message
            welcome_label = ctk.CTkLabel(
                home_frame,
                text=f"Bienvenido, {self.current_user.username}!",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            welcome_label.pack(pady=50)
            
            # System info
            info_label = ctk.CTkLabel(
                home_frame,
                text="Sistema de Gestión Escolar GES v1.0.0",
                font=ctk.CTkFont(size=16)
            )
            info_label.pack(pady=20)
            
            # Instructions
            instructions_text = """
            Use el menú lateral para navegar:
            
            Estudiantes - Gestión de estudiantes

            Matrículas - Matrículas y pagos

            Reportes - Gráficas e historial

            Ajustes - Configuración del sistema
            """
            
            instructions_label = ctk.CTkLabel(
                home_frame,
                text=instructions_text,
                font=ctk.CTkFont(size=12),
                justify="left"
            )
            instructions_label.pack(pady=30)
            
            self.views["home"] = home_frame
        
        # Mostrar vista home
        if self.current_view:
            self.current_view.grid_forget()
        
        self.current_view = self.views["home"]
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_students_view(self):
        """Show students management view"""
        self.show_view("students", StudentsView)
    
    def show_enrollments_view(self):
        """Show enrollments management view"""
        self.show_view("enrollments", EnrollmentsView)
    
    def show_reports_view(self):
        """Show reports management view"""
        self.show_view("reports", ReportsView)
    
    def show_settings_view(self):
        """Show settings management view"""
        self.show_view("settings", SettingsView)
    
    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.master.destroy()
    
    def handle_close(self):
        """Handle window close"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir de GES?"):
            self.master.destroy()


class MainApplication:
    """Main application wrapper"""
    
    def __init__(self, current_user: UserModel):
        self.current_user = current_user
        self.root = None
    
    def show(self):
        """Show main application"""
        # Create main window
        self.root = ctk.CTk()
        self.root.title(f"GES - {self.current_user.username}")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Center window on screen
        self.center_window()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.handle_close)
        
        # Create main view
        main_view = MainView(self.root, self.current_user)
        
        # Start window
        self.root.mainloop()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
    
    def handle_close(self):
        """Handle window close"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir de GES?"):
            self.root.destroy()


def main():
    """Test main view"""
    # Create a mock user for testing
    from database.models.person import UserRole
    
    mock_user = UserModel()
    mock_user.username = "test_user"
    mock_user.role = UserRole.ADMIN.value
    
    main_view = MainView(mock_user)
    main_view.show()


if __name__ == "__main__":
    main()
