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
        
        # NO usar pack(Mes estuvo provocando dolores de cabeza en la ui) aquí - dejar que MainApplication lo maneje
        # self.pack(fill="both", expand=True)
        
        # Layout principal
        self._build_layout()
    
    def _build_layout(self):
        """Build main layout"""
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar (columna 0)
        self.sidebar = Sidebar(self, on_menu_select=self.show_view)
        self.sidebar.frame.grid(row=0, column=0, sticky="nsew")
        
        # Contenedor central (columna 1)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Mostrar vista home por defecto
        self.show_home_view()
    
    def show_view(self, view_name: str, view_class):
        """
        Muestra una vista en el área central.
        Nunca destruye vistas, solo las oculta.
        Así evité el conflicto ese... qué dolor
        """
        
        # Handle special cases
        if view_name == "home":
            self.show_home_view()
            return
        
        if view_name == "logout":
            self.handle_logout()
            return
        
        # Ocultar vista actual
        if self.current_view:
            self.current_view.grid_remove()
        
        # Crear vista si no existe
        if view_name not in self.views:
            view = view_class(self.content_frame)
            view.grid(row=0, column=0, sticky="nsew")
            view.grid_remove()  # Ocultar inicialmente
            self.views[view_name] = view
        
        # Mostrar vista
        self.current_view = self.views[view_name]
        self.current_view_name = view_name
        self.current_view.grid()
    
    def show_home_view(self):
        """Show home dashboard"""
        # Ocultar vista actual
        if self.current_view:
            self.current_view.grid_remove()
        
        # Crear vista home si no existe
        if "home" not in self.views:
            home_frame = ctk.CTkFrame(self.content_frame)
            home_frame.grid(row=0, column=0, sticky="nsew")
            home_frame.grid_remove()  # Ocultar inicialmente
            
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
            
            📚 Estudiantes - Gestión de estudiantes
            📝 Matrículas - Matrículas y pagos
            📊 Reportes - Gráficas e historial
            ⚙️ Ajustes - Configuración del sistema
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
        self.current_view = self.views["home"]
        self.current_view_name = "home"
        self.current_view.grid()
    
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
        
        # Create main view - USAR PACK AQUÍ
        main_view = MainView(self.root, self.current_user)
        main_view.pack(fill="both", expand=True)
        
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