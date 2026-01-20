"""
Student form for GES application
Handles student creation and editing
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from typing import Optional, Dict, Any
from app.services.student_service import StudentService
from app.services.tutor_service import TutorService
from database.models.person import StudentModel, TutorModel


class StudentForm:
    """Form for creating and editing students"""
    
    def __init__(self, parent, student_service: StudentService, tutor_service: TutorService, student: Optional[StudentModel] = None):
        self.parent = parent
        self.student_service = student_service
        self.tutor_service = tutor_service
        self.student = student
        self.is_edit_mode = student is not None
        
        self.dialog = None
        self.result = False
        self.tutors = []
        
        self.load_tutors()
    
    def load_tutors(self):
        """Load available tutors"""
        try:
            self.tutors = self.tutor_service.get_all_tutors()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tutores: {str(e)}")
    
    def show(self) -> bool:
        """Show the form dialog"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Editar Estudiante" if self.is_edit_mode else "Nuevo Estudiante")
        self.dialog.geometry("500x600")
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
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (500 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
    
    def create_widgets(self):
        """Create form widgets"""
        # Main container with scroll
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = "Editar Estudiante" if self.is_edit_mode else "Nuevo Estudiante"
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Personal Information
        personal_frame = ctk.CTkFrame(main_frame)
        personal_frame.pack(fill="x", pady=(0, 15))
        
        personal_title = ctk.CTkLabel(
            personal_frame,
            text="Información Personal",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        personal_title.pack(pady=10)
        
        # Name
        name_label = ctk.CTkLabel(personal_frame, text="Nombre:")
        name_label.pack(anchor="w", padx=10)
        
        self.name_entry = ctk.CTkEntry(personal_frame, width=400)
        self.name_entry.pack(pady=5, padx=10)
        
        # Last name
        last_name_label = ctk.CTkLabel(personal_frame, text="Apellidos:")
        last_name_label.pack(anchor="w", padx=10)
        
        self.last_name_entry = ctk.CTkEntry(personal_frame, width=400)
        self.last_name_entry.pack(pady=5, padx=10)
        
        # Birth date
        birth_date_label = ctk.CTkLabel(personal_frame, text="Fecha de Nacimiento (YYYY-MM-DD):")
        birth_date_label.pack(anchor="w", padx=10)
        
        self.birth_date_entry = ctk.CTkEntry(personal_frame, width=400)
        self.birth_date_entry.pack(pady=5, padx=10)
        
        # Sex
        sex_label = ctk.CTkLabel(personal_frame, text="Sexo:")
        sex_label.pack(anchor="w", padx=10)
        
        self.sex_var = ctk.StringVar(value="M")
        sex_frame = ctk.CTkFrame(personal_frame)
        sex_frame.pack(pady=5, padx=10, fill="x")
        
        self.male_radio = ctk.CTkRadioButton(sex_frame, text="Masculino", variable=self.sex_var, value="M")
        self.male_radio.pack(side="left", padx=10)
        
        self.female_radio = ctk.CTkRadioButton(sex_frame, text="Femenino", variable=self.sex_var, value="F")
        self.female_radio.pack(side="left", padx=10)
        
        # Academic Information
        academic_frame = ctk.CTkFrame(main_frame)
        academic_frame.pack(fill="x", pady=(0, 15))
        
        academic_title = ctk.CTkLabel(
            academic_frame,
            text="Información Académica",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        academic_title.pack(pady=10)
        
        # Previous school
        previous_school_label = ctk.CTkLabel(academic_frame, text="Centro de Procedencia:")
        previous_school_label.pack(anchor="w", padx=10)
        
        self.previous_school_entry = ctk.CTkEntry(academic_frame, width=400)
        self.previous_school_entry.pack(pady=5, padx=10)
        
        # Tutor
        tutor_label = ctk.CTkLabel(academic_frame, text="Tutor:")
        tutor_label.pack(anchor="w", padx=10)
        
        self.tutor_var = ctk.StringVar()
        tutor_options = ["Seleccionar tutor..."] + [f"{t.person.name} {t.person.last_name}" if t.person else "Sin nombre" for t in self.tutors]
        self.tutor_combo = ctk.CTkComboBox(academic_frame, variable=self.tutor_var, values=tutor_options, width=400)
        self.tutor_combo.pack(pady=5, padx=10)
        
        # Contact Information
        contact_frame = ctk.CTkFrame(main_frame)
        contact_frame.pack(fill="x", pady=(0, 15))
        
        contact_title = ctk.CTkLabel(
            contact_frame,
            text="Información de Contacto",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        contact_title.pack(pady=10)
        
        # Email
        email_label = ctk.CTkLabel(contact_frame, text="Email:")
        email_label.pack(anchor="w", padx=10)
        
        self.email_entry = ctk.CTkEntry(contact_frame, width=400)
        self.email_entry.pack(pady=5, padx=10)
        
        # Phone
        phone_label = ctk.CTkLabel(contact_frame, text="Teléfono:")
        phone_label.pack(anchor="w", padx=10)
        
        self.phone_entry = ctk.CTkEntry(contact_frame, width=400)
        self.phone_entry.pack(pady=5, padx=10)
        
        # Address
        address_label = ctk.CTkLabel(contact_frame, text="Dirección:")
        address_label.pack(anchor="w", padx=10)
        
        self.address_entry = ctk.CTkTextbox(contact_frame, width=400, height=60)
        self.address_entry.pack(pady=5, padx=10)
        
        # Observations
        obs_label = ctk.CTkLabel(contact_frame, text="Observaciones:")
        obs_label.pack(anchor="w", padx=10)
        
        self.observations_entry = ctk.CTkTextbox(contact_frame, width=400, height=60)
        self.observations_entry.pack(pady=5, padx=10)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=15)
        
        self.save_button = ctk.CTkButton(
            buttons_frame,
            text="Guardar",
            command=self.save_student,
            width=100
        )
        self.save_button.pack(side="left", padx=10, pady=10)
        
        self.cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.cancel_form,
            width=100
        )
        self.cancel_button.pack(side="right", padx=10, pady=10)
        
        # Load data if editing
        if self.is_edit_mode:
            self.load_student_data()
    
    def load_student_data(self):
        """Load student data for editing"""
        if not self.student:
            return
        
        # Personal info
        if self.student.person:
            self.name_entry.insert(0, self.student.person.name or "")
            self.last_name_entry.insert(0, self.student.person.last_name or "")
            if self.student.person.birth_date:
                self.birth_date_entry.insert(0, self.student.person.birth_date.strftime("%Y-%m-%d"))
            self.email_entry.insert(0, self.student.person.email or "")
            self.phone_entry.insert(0, self.student.person.phone or "")
            if self.student.person.address:
                self.address_entry.insert("0.0", self.student.person.address)
        
        # Academic info
        self.previous_school_entry.insert(0, self.student.previous_school or "")
        
        # Medical info as observations
        if self.student.medical_info:
            self.observations_entry.insert("0.0", self.student.medical_info)
        
        # Sex (assuming it's stored in person or would need to be added)
        # For now, default to male
        self.sex_var.set("M")
    
    def validate_form(self) -> Dict[str, Any]:
        """Validate form and return data"""
        data = {}
        
        # Required fields
        name = self.name_entry.get().strip()
        if not name:
            raise ValueError("El nombre es obligatorio")
        data['name'] = name
        
        last_name = self.last_name_entry.get().strip()
        if not last_name:
            raise ValueError("Los apellidos son obligatorios")
        data['last_name'] = last_name
        
        # Birth date
        birth_date_str = self.birth_date_entry.get().strip()
        if not birth_date_str:
            raise ValueError("La fecha de nacimiento es obligatoria")
        
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            data['birth_date'] = birth_date
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
        
        # Optional fields
        data['sex'] = self.sex_var.get()
        data['previous_school'] = self.previous_school_entry.get().strip()
        data['email'] = self.email_entry.get().strip()
        data['phone'] = self.phone_entry.get().strip()
        data['address'] = self.address_entry.get("0.0", "end").strip()
        data['medical_info'] = self.observations_entry.get("0.0", "end").strip()
        
        # Tutor
        tutor_index = self.tutor_combo.current() - 1  # -1 because of "Seleccionar tutor..."
        if tutor_index >= 0 and tutor_index < len(self.tutors):
            data['tutor_id'] = self.tutors[tutor_index].id
        
        return data
    
    def save_student(self):
        """Save student data"""
        try:
            # Validate form
            data = self.validate_form()
            
            if self.is_edit_mode:
                # Update existing student
                update_data = {
                    'name': data['name'],
                    'last_name': data['last_name'],
                    'birth_date': data['birth_date'],
                    'previous_school': data['previous_school'],
                    'medical_info': data['medical_info']
                }
                
                # Would need to update person record too
                # For now, just update student
                self.student_service.update_student(self.student.id, update_data)
                messagebox.showinfo("Éxito", "Estudiante actualizado exitosamente")
            else:
                # Create new student
                self.student_service.create_student(data)
                messagebox.showinfo("Éxito", "Estudiante creado exitosamente")
            
            self.result = True
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar estudiante: {str(e)}")
    
    def cancel_form(self):
        """Cancel form"""
        self.dialog.destroy()
