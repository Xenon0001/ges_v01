"""
Students list view for GES application
Handles student listing and CRUD operations
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional
from app.services.student_service import StudentService
from app.services.tutor_service import TutorService
from database.models.person import StudentModel, TutorModel
from .student_form import StudentForm


class StudentsView(ctk.CTkFrame):
    """Students management view"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.student_service = StudentService()
        self.tutor_service = TutorService()
        self.current_students = []
        self.selected_student = None

        # NO usar pack aquí - el padre usa grid
        # self.pack(fill="both", expand=True)
        
        # Configurar grid para este frame
        self.grid_rowconfigure(4, weight=1)  # La fila del list_frame
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.load_students()
    
    def create_widgets(self):
        """Create students list view widgets"""
        # Header with title and actions
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Gestión de Estudiantes",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(header_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)
        
        self.new_button = ctk.CTkButton(
            buttons_frame,
            text="Nuevo Estudiante",
            command=self.create_student,
            width=120
        )
        self.new_button.pack(side="left", padx=5)
        
        self.edit_button = ctk.CTkButton(
            buttons_frame,
            text="Editar",
            command=self.edit_student,
            width=80,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=5)
        
        self.delete_button = ctk.CTkButton(
            buttons_frame,
            text="Eliminar",
            command=self.delete_student,
            width=80,
            state="disabled"
        )
        self.delete_button.pack(side="left", padx=5)
        
        self.refresh_button = ctk.CTkButton(
            buttons_frame,
            text="Actualizar",
            command=self.load_students,
            width=80
        )
        self.refresh_button.pack(side="left", padx=5)
        
        # Search frame
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        search_label = ctk.CTkLabel(search_frame, text="Buscar:")
        search_label.pack(side="left", padx=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nombre o ID del estudiante",
            width=300
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        self.search_button = ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_students,
            width=80
        )
        self.search_button.pack(side="left", padx=5)
        
        # Students list
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for students
        self.students_frame = ctk.CTkScrollableFrame(list_frame)
        self.students_frame.grid(row=0, column=0, sticky="nsew")
        
        # Status label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0, pady=5)
    
    def load_students(self):
        """Load all students"""
        try:
            self.current_students = self.student_service.search_students()
            self.display_students()
            self.update_status(f"Se cargaron {len(self.current_students)} estudiantes")
        except Exception as e:
            self.update_status(f"Error al cargar estudiantes: {str(e)}", error=True)
    
    def search_students(self):
        """Search students by name or ID"""
        search_term = self.search_entry.get().strip()
        try:
            if search_term:
                # Try to search by ID first, then by name
                if search_term.startswith('EST'):
                    students = [self.student_service.get_student_by_student_id(search_term)]
                    students = [s for s in students if s is not None]
                else:
                    students = self.student_service.search_students(name=search_term)
            else:
                students = self.student_service.search_students()
            
            self.current_students = students
            self.display_students()
            self.update_status(f"Se encontraron {len(students)} estudiantes")
        except Exception as e:
            self.update_status(f"Error en búsqueda: {str(e)}", error=True)
    
    def on_search_change(self, event):
        """Handle search entry change"""
        # Auto-search after typing stops (simple implementation)
        if hasattr(self, '_search_timer'):
            self.after_cancel(self._search_timer)
        self._search_timer = self.after(500, self.search_students)
    
    def display_students(self):
        """Display students in the list"""
        # Clear existing widgets
        for widget in self.students_frame.winfo_children():
            widget.destroy()
        
        if not self.current_students:
            no_students_label = ctk.CTkLabel(
                self.students_frame,
                text="No se encontraron estudiantes",
                font=ctk.CTkFont(size=14)
            )
            no_students_label.pack(pady=20)
            return
        
        # Create student cards
        for i, student in enumerate(self.current_students):
            self.create_student_card(student, i)
    
    def create_student_card(self, student: StudentModel, index: int):
        """Create a card for a student"""
        card_frame = ctk.CTkFrame(self.students_frame)
        card_frame.pack(fill="x", pady=5, padx=5)
        
        # Student info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Name and ID
        name_text = f"{student.person.name} {student.person.last_name}" if student.person else "Sin nombre"
        id_text = f"ID: {student.student_id}"
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=name_text,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(anchor="w")
        
        id_label = ctk.CTkLabel(
            info_frame,
            text=id_text,
            font=ctk.CTkFont(size=12)
        )
        id_label.pack(anchor="w")
        
        # Additional info
        if student.person and student.person.birth_date:
            from datetime import date
            age = (date.today() - student.person.birth_date).days // 365
            age_label = ctk.CTkLabel(
                info_frame,
                text=f"Edad: {age} años",
                font=ctk.CTkFont(size=11)
            )
            age_label.pack(anchor="w")
        
        # Select button
        select_button = ctk.CTkButton(
            card_frame,
            text="Seleccionar",
            width=80,
            command=lambda s=student: self.select_student(s)
        )
        select_button.pack(side="right", padx=10, pady=5)
        
        # Bind click event
        card_frame.bind("<Button-1>", lambda e, s=student: self.select_student(s))
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", lambda e, s=student: self.select_student(s))
    
    def select_student(self, student: StudentModel):
        """Select a student"""
        self.selected_student = student
        self.edit_button.configure(state="normal")
        self.delete_button.configure(state="normal")
        self.update_status(f"Seleccionado: {student.person.name if student.person else 'Sin nombre'}")
    
    def create_student(self):
        """Open form to create new student"""
        try:
            form = StudentForm(self.winfo_toplevel(), self.student_service, self.tutor_service)
            if form.show():
                self.load_students()
                self.update_status("Estudiante creado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear estudiante: {str(e)}")
    
    def edit_student(self):
        """Open form to edit selected student"""
        if not self.selected_student:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para editar")
            return
        
        try:
            form = StudentForm(
                self.winfo_toplevel(), 
                self.student_service, 
                self.tutor_service, 
                self.selected_student
            )
            if form.show():
                self.load_students()
                self.update_status("Estudiante actualizado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al editar estudiante: {str(e)}")
    
    def delete_student(self):
        """Delete selected student"""
        if not self.selected_student:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return
        
        student_name = self.selected_student.person.name if self.selected_student.person else "Este estudiante"
        
        if messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar al estudiante '{student_name}'?\n\nEsta acción no se puede deshacer."
        ):
            try:
                success = self.student_service.delete_student(self.selected_student.id)
                if success:
                    self.load_students()
                    self.selected_student = None
                    self.edit_button.configure(state="disabled")
                    self.delete_button.configure(state="disabled")
                    self.update_status("Estudiante eliminado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el estudiante")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar estudiante: {str(e)}")
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        if hasattr(self, '_status_timer'):
            self.after_cancel(self._status_timer)
        self._status_timer = self.after(5000, lambda: self.status_label.configure(text=""))