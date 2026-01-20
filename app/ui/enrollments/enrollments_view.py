"""
Enrollments list view for GES application
Handles enrollment listing and management
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService
from app.services.school_service import SchoolService
from database.models.enrollment import EnrollmentModel
from database.models.person import StudentModel
from database.models.school import GradeModel, AcademicYearModel
from .enrollment_form import EnrollmentForm
from .payments_view import PaymentsView


class EnrollmentsView(ctk.CTkFrame):
    """Enrollments management view"""
    
    def __init__(self, parent):
        super().__init__(parent)
        # NO usar pack aquí
        # self.pack(fill="both", expand=True)
        
        self.enrollment_service = EnrollmentService()
        self.student_service = StudentService()
        self.school_service = SchoolService()
        self.current_enrollments = []
        self.selected_enrollment = None
        
        # Data for filters
        self.academic_years = []
        self.grades = []
        
        # Configurar grid
        self.grid_rowconfigure(3, weight=1)  # La fila del list_frame
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create enrollments list view widgets"""
        # Header with title and actions
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Gestión de Matrículas",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(header_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)
        
        self.new_button = ctk.CTkButton(
            buttons_frame,
            text="Nueva Matrícula",
            command=self.create_enrollment,
            width=120
        )
        self.new_button.pack(side="left", padx=5)
        
        self.payments_button = ctk.CTkButton(
            buttons_frame,
            text="Ver Pagos",
            command=self.view_payments,
            width=100,
            state="disabled"
        )
        self.payments_button.pack(side="left", padx=5)
        
        self.refresh_button = ctk.CTkButton(
            buttons_frame,
            text="Actualizar",
            command=self.load_data,
            width=80
        )
        self.refresh_button.pack(side="left", padx=5)
        
        # Filters frame
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        filters_label = ctk.CTkLabel(filters_frame, text="Filtros:", font=ctk.CTkFont(size=14, weight="bold"))
        filters_label.pack(anchor="w", padx=10, pady=5)
        
        # Academic year filter
        year_frame = ctk.CTkFrame(filters_frame)
        year_frame.pack(fill="x", padx=10, pady=5)
        
        year_label = ctk.CTkLabel(year_frame, text="Año Académico:")
        year_label.pack(side="left", padx=5)
        
        self.year_var = ctk.StringVar()
        self.year_combo = ctk.CTkComboBox(year_frame, variable=self.year_var, width=200)
        self.year_combo.pack(side="left", padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_enrollments())
        
        # Grade filter
        grade_label = ctk.CTkLabel(year_frame, text="Grado:")
        grade_label.pack(side="left", padx=5)
        
        self.grade_var = ctk.StringVar()
        self.grade_combo = ctk.CTkComboBox(year_frame, variable=self.grade_var, width=200)
        self.grade_combo.pack(side="left", padx=5)
        self.grade_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_enrollments())
        
        # Clear filters button
        clear_button = ctk.CTkButton(
            year_frame,
            text="Limpiar Filtros",
            command=self.clear_filters,
            width=100
        )
        clear_button.pack(side="right", padx=5)
        
        # Enrollments list
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for enrollments
        self.enrollments_frame = ctk.CTkScrollableFrame(list_frame)
        self.enrollments_frame.grid(row=0, column=0, sticky="nsew")
        
        # Status label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0, pady=5)
    
    def load_data(self):
        """Load all data for enrollments view"""
        try:
            # Load academic years
            self.academic_years = self.school_service.get_academic_years()
            year_options = ["Todos"] + [ay.name for ay in self.academic_years]
            self.year_combo.configure(values=year_options)
            if year_options:
                self.year_combo.set(year_options[0])
            
            # Load grades
            self.grades = self.school_service.get_grades()
            grade_options = ["Todos"] + [g.name for g in self.grades]
            self.grade_combo.configure(values=grade_options)
            if grade_options:
                self.grade_combo.set(grade_options[0])
            
            # Load enrollments
            self.load_enrollments()
            
        except Exception as e:
            self.update_status(f"Error al cargar datos: {str(e)}", error=True)
    
    def load_enrollments(self):
        """Load enrollments based on current filters"""
        try:
            # Get filter values
            academic_year_id = None
            grade_id = None
            
            if self.year_var.get() and self.year_var.get() != "Todos":
                for ay in self.academic_years:
                    if ay.name == self.year_var.get():
                        academic_year_id = ay.id
                        break
            
            if self.grade_var.get() and self.grade_var.get() != "Todos":
                for grade in self.grades:
                    if grade.name == self.grade_var.get():
                        grade_id = grade.id
                        break
            
            # Get enrollments
            self.current_enrollments = self.enrollment_service.get_enrollments_by_filters(
                academic_year_id=academic_year_id,
                grade_id=grade_id
            )
            
            self.display_enrollments()
            self.update_status(f"Se cargaron {len(self.current_enrollments)} matrículas")
            
        except Exception as e:
            self.update_status(f"Error al cargar matrículas: {str(e)}", error=True)
    
    def filter_enrollments(self):
        """Filter enrollments based on selected filters"""
        self.load_enrollments()
    
    def clear_filters(self):
        """Clear all filters"""
        self.year_combo.set("Todos")
        self.grade_combo.set("Todos")
        self.load_enrollments()
    
    def display_enrollments(self):
        """Display enrollments in list"""
        # Clear existing widgets
        for widget in self.enrollments_frame.winfo_children():
            widget.destroy()
        
        if not self.current_enrollments:
            no_enrollments_label = ctk.CTkLabel(
                self.enrollments_frame,
                text="No se encontraron matrículas",
                font=ctk.CTkFont(size=14)
            )
            no_enrollments_label.pack(pady=20)
            return
        
        # Create enrollment cards
        for i, enrollment in enumerate(self.current_enrollments):
            self.create_enrollment_card(enrollment, i)
    
    def create_enrollment_card(self, enrollment: EnrollmentModel, index: int):
        """Create a card for an enrollment"""
        card_frame = ctk.CTkFrame(self.enrollments_frame)
        card_frame.pack(fill="x", pady=5, padx=5)
        
        # Enrollment info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Student name and enrollment number
        student_name = "Estudiante no encontrado"
        if enrollment.student and enrollment.student.person:
            student_name = f"{enrollment.student.person.name} {enrollment.student.person.last_name}"
        
        enrollment_text = f"{student_name}"
        number_text = f"Matrícula: {enrollment.enrollment_number}"
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=enrollment_text,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(anchor="w")
        
        number_label = ctk.CTkLabel(
            info_frame,
            text=number_text,
            font=ctk.CTkFont(size=12)
        )
        number_label.pack(anchor="w")
        
        # Additional info
        grade_name = enrollment.grade.name if enrollment.grade else "Sin grado"
        year_name = enrollment.academic_year.name if enrollment.academic_year else "Sin año"
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"{grade_name} - {year_name}",
            font=ctk.CTkFont(size=11)
        )
        details_label.pack(anchor="w")
        
        # Status
        status_color = "green" if enrollment.status == "active" else "orange"
        status_label = ctk.CTkLabel(
            info_frame,
            text=f"Estado: {enrollment.status}",
            font=ctk.CTkFont(size=11),
            text_color=status_color
        )
        status_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card_frame)
        actions_frame.pack(side="right", padx=10, pady=5)
        
        select_button = ctk.CTkButton(
            actions_frame,
            text="Seleccionar",
            width=80,
            command=lambda e=enrollment: self.select_enrollment(e)
        )
        select_button.pack(pady=2)
        
        payments_button = ctk.CTkButton(
            actions_frame,
            text="Pagos",
            width=80,
            command=lambda e=enrollment: self.view_enrollment_payments(e)
        )
        payments_button.pack(pady=2)
        
        # Bind click event
        card_frame.bind("<Button-1>", lambda e, en=enrollment: self.select_enrollment(en))
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", lambda e, en=enrollment: self.select_enrollment(en))
    
    def select_enrollment(self, enrollment: EnrollmentModel):
        """Select an enrollment"""
        self.selected_enrollment = enrollment
        self.payments_button.configure(state="normal")
        student_name = "Estudiante no encontrado"
        if enrollment.student and enrollment.student.person:
            student_name = enrollment.student.person.name
        self.update_status(f"Seleccionada matrícula de: {student_name}")
    
    def create_enrollment(self):
        """Open form to create new enrollment"""
        try:
            form = EnrollmentForm(
                self.winfo_toplevel(), 
                self.enrollment_service, 
                self.student_service, 
                self.school_service
            )
            if form.show():
                self.load_enrollments()
                self.update_status("Matrícula creada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear matrícula: {str(e)}")
    
    def view_payments(self):
        """View payments for selected enrollment"""
        if not self.selected_enrollment:
            messagebox.showwarning("Advertencia", "Seleccione una matrícula para ver sus pagos")
            return
        
        self.view_enrollment_payments(self.selected_enrollment)
    
    def view_enrollment_payments(self, enrollment: EnrollmentModel):
        """View payments for specific enrollment"""
        try:
            # Ocultar esta vista
            self.grid_remove()
            
            # Crear vista de pagos en el mismo padre
            payments_view = PaymentsView(self.master, enrollment, self.enrollment_service, self)
            payments_view.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir pagos: {str(e)}")
            self.grid()  # Restaurar esta vista si hay error
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        if hasattr(self, '_status_timer'):
            self.after_cancel(self._status_timer)
        self._status_timer = self.after(5000, lambda: self.status_label.configure(text=""))