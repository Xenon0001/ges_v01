import customtkinter as ctk
from tkinter import messagebox, ttk
from services.student_service import StudentService
from services.grade_service import GradeService
from database.models import StudentModel, UserModel


class MainWindow:
    def __init__(self, current_user: UserModel):
        self.current_user = current_user
        self.student_service = StudentService()
        self.grade_service = GradeService()
        self.root = None
        
        # Cache system for views
        self.views = {}
        self.current_view = None
        self.navigation_history = []
        
    def create_window(self):
        """Create main application window"""
        self.root = ctk.CTk()
        self.root.title("GES - Sistema de Gestión Escolar")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Main content area
        self.create_main_content()
        
        return self.root
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar_frame = ctk.CTkFrame(self.root, width=250)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        sidebar_frame.grid_rowconfigure(10, weight=1)
        
        # User info
        user_frame = ctk.CTkFrame(sidebar_frame)
        user_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        user_label = ctk.CTkLabel(
            user_frame, 
            text=f"Usuario: {self.current_user.username}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        user_label.grid(row=0, column=0, padx=10, pady=5)
        
        role_label = ctk.CTkLabel(
            user_frame, 
            text=f"Rol: {self.current_user.role}",
            font=ctk.CTkFont(size=12)
        )
        role_label.grid(row=1, column=0, padx=10, pady=(0, 5))
        
        # Navigation buttons
        ctk.CTkButton(
            sidebar_frame, 
            text="Estudiantes", 
            command=self.show_students,
            height=40
        ).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            sidebar_frame, 
            text="Notas", 
            command=self.show_grades,
            height=40
        ).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            sidebar_frame, 
            text="Reportes", 
            command=self.show_reports,
            height=40
        ).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            sidebar_frame, 
            text="Configuración", 
            command=self.show_settings,
            height=40
        ).grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        
        # Logout button
        ctk.CTkButton(
            sidebar_frame, 
            text="Cerrar Sesión", 
            command=self.logout,
            height=40,
            fg_color="red"
        ).grid(row=11, column=0, padx=10, pady=5, sticky="ew")
    
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Panel Principal",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_content(self):
        """Hide content frame instead of destroying it"""
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
    
    def show_view(self, view_name: str, view_creator):
        """Show a view using cache pattern"""
        # Hide current view
        if self.current_view:
            self.current_view.grid_forget()
        
        # Create view if not cached
        if view_name not in self.views:
            self.views[view_name] = view_creator()
        
        # Show new view
        self.current_view = self.views[view_name]
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def go_back(self):
        """Go back to previous view"""
        if self.navigation_history:
            prev_view_name = self.navigation_history.pop()
            self.show_view(prev_view_name, lambda: self.views[prev_view_name])
    
    def show_dashboard(self):
        """Show dashboard"""
        self.title_label.configure(text="Panel Principal")
        
        def create_dashboard():
            dashboard_frame = ctk.CTkFrame(self.content_frame)
            
            welcome_label = ctk.CTkLabel(
                dashboard_frame,
                text=f"Bienvenido al Sistema de Gestión Escolar",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            welcome_label.pack(pady=20)
            
            info_label = ctk.CTkLabel(
                dashboard_frame,
                text="Seleccione una opción del menú lateral para comenzar.",
                font=ctk.CTkFont(size=14)
            )
            info_label.pack(pady=10)
            
            return dashboard_frame
        
        self.show_view("dashboard", create_dashboard)
    
    def create_students_table(self, parent):
        """Create students table"""
        # Table frame
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview for students
        self.students_tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Nombre", "Apellido", "ID Estudiante", "Grado"),
            show="headings"
        )
        
        # Configure columns
        self.students_tree.heading("ID", text="ID")
        self.students_tree.heading("Nombre", text="Nombre")
        self.students_tree.heading("Apellido", text="Apellido")
        self.students_tree.heading("ID Estudiante", text="ID Estudiante")
        self.students_tree.heading("Grado", text="Grado")
        
        self.students_tree.column("ID", width=50)
        self.students_tree.column("Nombre", width=150)
        self.students_tree.column("Apellido", width=150)
        self.students_tree.column("ID Estudiante", width=120)
        self.students_tree.column("Grado", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Load students
        self.refresh_students()
    
    def refresh_students(self):
        """Refresh students list"""
        if hasattr(self, 'students_tree'):
            # Clear existing items
            for item in self.students_tree.get_children():
                self.students_tree.delete(item)
            
            # Load students
            try:
                students = self.student_service.get_all_students()
                for student in students:
                    self.students_tree.insert(
                        "",
                        "end",
                        values=(
                            student.id,
                            student.name,
                            student.last_name,
                            student.student_id,
                            student.grade or "N/A"
                        )
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")
    
    def add_student(self):
        """Add new student (placeholder)"""
        messagebox.showinfo("Información", "Función de agregar estudiante en desarrollo")
    
    def show_students(self):
        """Show students management"""
        self.title_label.configure(text="Gestión de Estudiantes")
        
        def create_students_view():
            students_frame = ctk.CTkFrame(self.content_frame)
            students_frame.grid_columnconfigure(0, weight=1)
            students_frame.grid_rowconfigure(1, weight=1)
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(students_frame)
            buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            ctk.CTkButton(
                buttons_frame,
                text="Nuevo Estudiante",
                command=self.add_student,
                width=150
            ).grid(row=0, column=0, padx=5, pady=5)
            
            ctk.CTkButton(
                buttons_frame,
                text="Actualizar Lista",
                command=self.refresh_students,
                width=150
            ).grid(row=0, column=1, padx=5, pady=5)
            
            # Students list
            self.create_students_table(students_frame)
            return students_frame
        
        self.show_view("students", create_students_view)
    
    def show_grades(self):
        """Show grades management"""
        self.title_label.configure(text="Gestión de Notas")
        
        def create_grades_view():
            grades_frame = ctk.CTkFrame(self.content_frame)
            
            info_label = ctk.CTkLabel(
                grades_frame,
                text="Gestión de Notas - En desarrollo",
                font=ctk.CTkFont(size=16)
            )
            info_label.pack(padx=20, pady=20)
            
            return grades_frame
        
        self.show_view("grades", create_grades_view)
    
    def show_reports(self):
        """Show reports"""
        self.title_label.configure(text="Reportes")
        
        def create_reports_view():
            reports_frame = ctk.CTkFrame(self.content_frame)
            
            info_label = ctk.CTkLabel(
                reports_frame,
                text="Reportes - En desarrollo",
                font=ctk.CTkFont(size=16)
            )
            info_label.pack(padx=20, pady=20)
            
            return reports_frame
        
        self.show_view("reports", create_reports_view)
    
    def show_settings(self):
        """Show settings"""
        self.title_label.configure(text="Configuración")
        
        def create_settings_view():
            settings_frame = ctk.CTkFrame(self.content_frame)
            
            info_label = ctk.CTkLabel(
                settings_frame,
                text="Configuración - En desarrollo",
                font=ctk.CTkFont(size=16)
            )
            info_label.pack(padx=20, pady=20)
            
            return settings_frame
        
        self.show_view("settings", create_settings_view)
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            # Return to login
            from ui.login_window import LoginWindow
            login_window = LoginWindow()
            login_window.run(self.on_login_success)
    
    def on_login_success(self, user):
        """Handle successful login"""
        main_window = MainWindow(user)
        window = main_window.create_window()
        window.mainloop()
    
    def run(self):
        """Run the main window"""
        window = self.create_window()
        window.mainloop()
