"""
Enrollment form for GES application
Handles student enrollment creation
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService
from app.services.school_service import SchoolService
from database.models.enrollment import EnrollmentModel
from database.models.person import StudentModel
from database.models.school import GradeModel, AcademicYearModel


class EnrollmentForm:
    """Form for creating student enrollments"""
    
    def __init__(self, parent, enrollment_service: EnrollmentService, 
                 student_service: StudentService, school_service: SchoolService):
        self.parent = parent
        self.enrollment_service = enrollment_service
        self.student_service = student_service
        self.school_service = school_service
        
        self.dialog = None
        self.result = False
        
        # Data for dropdowns
        self.students = []
        self.academic_years = []
        self.grades = []
        
        self.load_data()
    
    def load_data(self):
        """Load data for form dropdowns"""
        try:
            self.students = self.student_service.search_students()
            self.academic_years = self.school_service.get_academic_years()
            self.grades = self.school_service.get_grades()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def show(self) -> bool:
        """Show enrollment form dialog"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Nueva Matrícula")
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.center_dialog()
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
        return self.result
    
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (600 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")
    
    def create_widgets(self):
        """Create form widgets"""
        # Main container with scroll
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Nueva Matrícula",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Student Selection
        student_frame = ctk.CTkFrame(main_frame)
        student_frame.pack(fill="x", pady=(0, 15))
        
        student_title = ctk.CTkLabel(
            student_frame,
            text="Información del Estudiante",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        student_title.pack(pady=10)
        
        # Student dropdown
        student_label = ctk.CTkLabel(student_frame, text="Estudiante:")
        student_label.pack(anchor="w", padx=10)
        
        self.student_var = ctk.StringVar()
        student_options = ["Seleccionar estudiante..."] + [
            f"{s.student_id} - {s.person.name} {s.person.last_name}" 
            if s.person else f"{s.student_id} - Sin nombre"
            for s in self.students
        ]
        self.student_combo = ctk.CTkComboBox(
            student_frame, 
            variable=self.student_var, 
            values=student_options, 
            width=500
        )
        self.student_combo.pack(pady=5, padx=10)
        self.student_combo.bind("<<ComboboxSelected>>", self.on_student_selected)
        
        # Student info display
        self.student_info_frame = ctk.CTkFrame(student_frame)
        self.student_info_frame.pack(fill="x", padx=10, pady=5)
        
        self.student_info_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Seleccione un estudiante para ver información",
            font=ctk.CTkFont(size=11)
        )
        self.student_info_label.pack(pady=5)
        
        # Academic Information
        academic_frame = ctk.CTkFrame(main_frame)
        academic_frame.pack(fill="x", pady=(0, 15))
        
        academic_title = ctk.CTkLabel(
            academic_frame,
            text="Información Académica",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        academic_title.pack(pady=10)
        
        # Academic Year
        year_label = ctk.CTkLabel(academic_frame, text="Año Académico:")
        year_label.pack(anchor="w", padx=10)
        
        self.year_var = ctk.StringVar()
        year_options = [ay.name for ay in self.academic_years]
        self.year_combo = ctk.CTkComboBox(
            academic_frame, 
            variable=self.year_var, 
            values=year_options, 
            width=500
        )
        self.year_combo.pack(pady=5, padx=10)
        
        # Grade
        grade_label = ctk.CTkLabel(academic_frame, text="Grado:")
        grade_label.pack(anchor="w", padx=10)
        
        self.grade_var = ctk.StringVar()
        grade_options = [g.name for g in self.grades]
        self.grade_combo = ctk.CTkComboBox(
            academic_frame, 
            variable=self.grade_var, 
            values=grade_options, 
            width=500
        )
        self.grade_combo.pack(pady=5, padx=10)
        
        # Course and Classroom
        course_frame = ctk.CTkFrame(academic_frame)
        course_frame.pack(fill="x", padx=10, pady=5)
        
        # Course
        course_label = ctk.CTkLabel(course_frame, text="Curso:")
        course_label.pack(side="left", padx=5)
        
        self.course_entry = ctk.CTkEntry(course_frame, width=200)
        self.course_entry.pack(side="left", padx=5)
        
        # Classroom
        classroom_label = ctk.CTkLabel(course_frame, text="Aula:")
        classroom_label.pack(side="left", padx=5)
        
        self.classroom_entry = ctk.CTkEntry(course_frame, width=200)
        self.classroom_entry.pack(side="left", padx=5)
        
        # Shift
        shift_label = ctk.CTkLabel(academic_frame, text="Turno:")
        shift_label.pack(anchor="w", padx=10)
        
        self.shift_var = ctk.StringVar(value="Mañana")
        shift_frame = ctk.CTkFrame(academic_frame)
        shift_frame.pack(pady=5, padx=10, fill="x")
        
        self.morning_radio = ctk.CTkRadioButton(
            shift_frame, 
            text="Mañana", 
            variable=self.shift_var, 
            value="Mañana"
        )
        self.morning_radio.pack(side="left", padx=10)
        
        self.afternoon_radio = ctk.CTkRadioButton(
            shift_frame, 
            text="Tarde", 
            variable=self.shift_var, 
            value="Tarde"
        )
        self.afternoon_radio.pack(side="left", padx=10)
        
        # Financial Information
        financial_frame = ctk.CTkFrame(main_frame)
        financial_frame.pack(fill="x", pady=(0, 15))
        
        financial_title = ctk.CTkLabel(
            financial_frame,
            text="Información Financiera",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        financial_title.pack(pady=10)
        
        # Total amount
        amount_frame = ctk.CTkFrame(financial_frame)
        amount_frame.pack(fill="x", padx=10, pady=5)
        
        amount_label = ctk.CTkLabel(amount_frame, text="Monto Total de Matrícula:")
        amount_label.pack(side="left", padx=5)
        
        self.amount_entry = ctk.CTkEntry(amount_frame, width=200)
        self.amount_entry.pack(side="left", padx=5)
        self.amount_entry.insert(0, "50000")  # Default amount
        
        # Initial payment
        initial_label = ctk.CTkLabel(amount_frame, text="Pago Inicial:")
        initial_label.pack(side="left", padx=5)
        
        self.initial_entry = ctk.CTkEntry(amount_frame, width=200)
        self.initial_entry.pack(side="left", padx=5)
        self.initial_entry.insert(0, "0")  # Default no initial payment
        
        # Payment Calendar Options
        calendar_frame = ctk.CTkFrame(financial_frame)
        calendar_frame.pack(fill="x", padx=10, pady=5)
        
        self.use_existing_calendar_var = ctk.BooleanVar(value=False)
        self.use_calendar_checkbox = ctk.CTkCheckBox(
            calendar_frame,
            text="Usar calendario de pagos existente del tutor",
            variable=self.use_existing_calendar_var,
            command=self.toggle_calendar_options
        )
        self.use_calendar_checkbox.pack(anchor="w", pady=5)
        
        # Additional Information
        additional_frame = ctk.CTkFrame(main_frame)
        additional_frame.pack(fill="x", pady=(0, 15))
        
        additional_title = ctk.CTkLabel(
            additional_frame,
            text="Información Adicional",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        additional_title.pack(pady=10)
        
        # Observations
        obs_label = ctk.CTkLabel(additional_frame, text="Observaciones:")
        obs_label.pack(anchor="w", padx=10)
        
        self.observations_entry = ctk.CTkTextbox(additional_frame, width=500, height=80)
        self.observations_entry.pack(pady=5, padx=10)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=15)
        
        self.save_button = ctk.CTkButton(
            buttons_frame,
            text="Crear Matrícula",
            command=self.save_enrollment,
            width=120
        )
        self.save_button.pack(side="left", padx=10, pady=10)
        
        self.cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel_form,
            width=100
        )
        self.cancel_button.pack(side="right", padx=10, pady=10)
        
        # Set default values if available
        if year_options:
            self.year_combo.set(year_options[0])
        if grade_options:
            self.grade_combo.set(grade_options[0])
    
    def on_student_selected(self, event):
        """Handle student selection"""
        student_index = self.student_combo.current() - 1  # -1 because of "Seleccionar estudiante..."
        if student_index >= 0 and student_index < len(self.students):
            student = self.students[student_index]
            self.display_student_info(student)
    
    def display_student_info(self, student: StudentModel):
        """Display selected student information"""
        if student.person:
            age = "Desconocida"
            if student.person.birth_date:
                age = (date.today() - student.person.birth_date).days // 365
            
            info_text = f"Edad: {age} años"
            if student.person.phone:
                info_text += f" | Tel: {student.person.phone}"
            if student.person.email:
                info_text += f" | Email: {student.person.email}"
            
            self.student_info_label.configure(text=info_text)
        else:
            self.student_info_label.configure(text="Información del estudiante no disponible")
    
    def toggle_calendar_options(self):
        """Toggle calendar options visibility"""
        # This would show/hide additional calendar selection options
        # For now, just a simple implementation
        pass
    
    def validate_form(self) -> Dict[str, Any]:
        """Validate form and return data"""
        data = {}
        
        # Student
        student_index = self.student_combo.current() - 1
        if student_index < 0:
            raise ValueError("Debe seleccionar un estudiante")
        data['student_id'] = self.students[student_index].id
        
        # Academic year
        year_name = self.year_var.get()
        if not year_name:
            raise ValueError("Debe seleccionar un año académico")
        
        year_id = None
        for ay in self.academic_years:
            if ay.name == year_name:
                year_id = ay.id
                break
        
        if not year_id:
            raise ValueError("Año académico no válido")
        data['academic_year_id'] = year_id
        
        # Grade
        grade_name = self.grade_var.get()
        if not grade_name:
            raise ValueError("Debe seleccionar un grado")
        
        grade_id = None
        for grade in self.grades:
            if grade.name == grade_name:
                grade_id = grade.id
                break
        
        if not grade_id:
            raise ValueError("Grado no válido")
        data['grade_id'] = grade_id
        
        # Course and classroom
        data['course'] = self.course_entry.get().strip()
        data['classroom'] = self.classroom_entry.get().strip()
        
        # Shift
        data['shift'] = self.shift_var.get()
        
        # Financial
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("El monto debe ser mayor a 0")
            data['total_amount'] = amount
        except ValueError:
            raise ValueError("Monto inválido")
        
        try:
            initial = float(self.initial_entry.get())
            if initial < 0:
                raise ValueError("El pago inicial no puede ser negativo")
            data['initial_payment'] = initial
        except ValueError:
            raise ValueError("Pago inicial inválido")
        
        # Observations
        data['observations'] = self.observations_entry.get("0.0", "end").strip()
        
        # Calendar option
        data['use_existing_calendar'] = self.use_existing_calendar_var.get()
        
        return data
    
    def save_enrollment(self):
        """Save enrollment data"""
        try:
            # Validate form
            data = self.validate_form()
            
            # Create enrollment
            enrollment = self.enrollment_service.enroll_student(
                student_id=data['student_id'],
                grade_id=data['grade_id'],
                academic_year_id=data['academic_year_id']
            )
            
            # Update additional fields
            update_data = {
                'course': data['course'],
                'classroom': data['classroom'],
                'shift': data['shift'],
                'observations': data['observations']
            }
            
            self.enrollment_service.update_enrollment(enrollment.id, update_data)
            
            # If initial payment, register it
            if data['initial_payment'] > 0:
                from app.services.payment_service import PaymentService
                payment_service = PaymentService()
                
                payment_service.register_payment(
                    enrollment_id=enrollment.id,
                    amount=data['initial_payment'],
                    description="Pago inicial de matrícula",
                    payment_method="cash"
                )
            
            messagebox.showinfo("Éxito", "Matrícula creada exitosamente")
            self.result = True
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear matrícula: {str(e)}")
    
    def cancel_form(self):
        """Cancel form"""
        self.dialog.destroy()
