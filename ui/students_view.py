"""
Students View - Gestión completa de estudiantes
CRUD profesional con tabla y formularios
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Optional
from datetime import datetime

from services.student_service import StudentService
from database.repository import classroom_repo


class StudentsView:
    """Vista de gestión de estudiantes"""
    
    def __init__(self, parent: tk.Frame, config: Dict[str, Any], 
                 student_service=None):
        self.parent = parent
        self.config = config
        self.student_service = student_service if student_service else StudentService()
        
        # Estado
        self.current_students = []
        self.selected_student_id = None
        
        # Crear UI
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_students()
    
    def create_widgets(self):
        """Crea todos los widgets"""
        # Header
        self.create_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.parent, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Barra de herramientas
        self.create_toolbar(main_container)
        
        # Tabla de estudiantes
        self.create_students_table(main_container)
        
        # Frame de detalles (inicialmente oculto)
        self.details_frame = None
    
    def create_header(self):
        """Crea el header de la vista"""
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="👥 Gestión de Estudiantes",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        # Botón de ayuda
        help_btn = tk.Button(
            header_frame,
            text="❓",
            font=('Segoe UI', 12),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.show_help
        )
        help_btn.pack(side='right', padx=20, pady=15)
    
    def create_toolbar(self, parent):
        """Crea la barra de herramientas"""
        toolbar_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        toolbar_frame.pack(fill='x', pady=(0, 10))
        
        # Contenedor izquierdo - acciones
        left_frame = tk.Frame(toolbar_frame, bg='white')
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        # Botones de acción
        self.create_toolbar_button(left_frame, "➕ Nuevo Estudiante", self.create_student, '#27ae60')
        self.create_toolbar_button(left_frame, "✏️ Editar", self.edit_student, '#3498db')
        self.create_toolbar_button(left_frame, "🗑️ Eliminar", self.delete_student, '#e74c3c')
        
        # Separador
        separator = tk.Frame(toolbar_frame, width=2, bg='#bdc3c7')
        separator.pack(side='left', fill='y', padx=10)
        
        # Contenedor derecho - búsqueda y filtros
        right_frame = tk.Frame(toolbar_frame, bg='white')
        right_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        # Campo de búsqueda
        search_label = tk.Label(right_frame, text="Buscar:", font=('Segoe UI', 10), bg='white')
        search_label.pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            right_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            width=20
        )
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_students())
        
        # Botón de búsqueda
        search_btn = tk.Button(
            right_frame,
            text="🔍",
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.filter_students
        )
        search_btn.pack(side='left')
        
        # Botón de refrescar
        refresh_btn = tk.Button(
            right_frame,
            text="🔄",
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.load_students
        )
        refresh_btn.pack(side='left', padx=(5, 0))
    
    def create_toolbar_button(self, parent, text: str, command, color: str):
        """Crea un botón de la barra de herramientas"""
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 9),
            bg=color,
            fg='white',
            relief='flat',
            cursor='hand2',
            command=command,
            padx=10,
            pady=5
        )
        btn.pack(side='left', padx=2)
        
        # Efecto hover
        btn.bind('<Enter>', lambda e: btn.configure(bg=self.darken_color(color)))
        btn.bind('<Leave>', lambda e: btn.configure(bg=color))
        
        return btn
    
    def create_students_table(self, parent):
        """Crea la tabla de estudiantes"""
        # Frame de la tabla
        table_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview (tabla)
        self.students_tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Nombre', 'Apellido', 'Aula', 'Estado', 'Tutor'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar columnas
        self.students_tree.heading('ID', text='ID')
        self.students_tree.heading('Nombre', text='Nombre')
        self.students_tree.heading('Apellido', text='Apellido')
        self.students_tree.heading('Aula', text='Aula')
        self.students_tree.heading('Estado', text='Estado')
        self.students_tree.heading('Tutor', text='Tutor')
        
        # Configurar anchos
        self.students_tree.column('ID', width=50, minwidth=50)
        self.students_tree.column('Nombre', width=150, minwidth=100)
        self.students_tree.column('Apellido', width=150, minwidth=100)
        self.students_tree.column('Aula', width=100, minwidth=80)
        self.students_tree.column('Estado', width=100, minwidth=80)
        self.students_tree.column('Tutor', width=200, minwidth=150)
        
        # Empaquetar
        self.students_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configurar grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Eventos
        self.students_tree.bind('<<TreeviewSelect>>', self.on_student_select)
        self.students_tree.bind('<Double-1>', lambda e: self.edit_student())
    
    def load_students(self):
        """Carga todos los estudiantes"""
        try:
            self.current_students = self.student_service.get_active_students()
            self.populate_table()
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar los estudiantes. Por favor, intente nuevamente.")
    
    def populate_table(self):
        """Llena la tabla con los estudiantes"""
        # Limpiar tabla
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Agregar estudiantes
        for student in self.current_students:
            # Obtener nombre del aula
            classroom_name = "Sin asignar"
            if student.get('classroom_id'):
                classroom = classroom_repo.get_by_id(student['classroom_id'])
                if classroom:
                    classroom_name = classroom['name']
            
            # Insertar en tabla
            self.students_tree.insert('', 'end', values=(
                student['id'],
                student['first_name'],
                student['last_name'],
                classroom_name,
                student['enrollment_status'],
                student.get('tutor_name', 'No especificado')
            ))
    
    def filter_students(self):
        """Filtra estudiantes según búsqueda"""
        search_term = self.search_var.get().lower().strip()
        
        if not search_term:
            self.populate_table()
            return
        
        # Filtrar estudiantes
        filtered_students = []
        for student in self.current_students:
            if (search_term in student['first_name'].lower() or 
                search_term in student['last_name'].lower() or
                search_term in student.get('tutor_name', '').lower()):
                filtered_students.append(student)
        
        # Actualizar tabla
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        for student in filtered_students:
            classroom_name = "Sin asignar"
            if student.get('classroom_id'):
                classroom = classroom_repo.get_by_id(student['classroom_id'])
                if classroom:
                    classroom_name = classroom['name']
            
            self.students_tree.insert('', 'end', values=(
                student['id'],
                student['first_name'],
                student['last_name'],
                classroom_name,
                student['enrollment_status'],
                student.get('tutor_name', 'No especificado')
            ))
    
    def on_student_select(self, event):
        """Maneja la selección de un estudiante"""
        selection = self.students_tree.selection()
        if selection:
            item = self.students_tree.item(selection[0])
            values = item['values']
            self.selected_student_id = values[0]
        else:
            self.selected_student_id = None
    
    def create_student(self):
        """Crea un nuevo estudiante"""
        self.show_student_form()
    
    def edit_student(self):
        """Edita el estudiante seleccionado"""
        if not self.selected_student_id:
            messagebox.showwarning("Selección Requerida", 
                               "Por favor seleccione un estudiante para editar")
            return
        
        # Buscar estudiante
        student = None
        for s in self.current_students:
            if s['id'] == self.selected_student_id:
                student = s
                break
        
        if student:
            self.show_student_form(student)
    
    def delete_student(self):
        """Elimina el estudiante seleccionado"""
        if not self.selected_student_id:
            messagebox.showwarning("Selección Requerida", 
                               "Por favor seleccione un estudiante para eliminar")
            return
        
        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Está seguro que desea eliminar este estudiante?\n\n" +
            "Esta acción cambiará el estado a 'retirado' y no se podrá deshacer."
        )
        
        if result:
            try:
                success = self.student_service.delete_student(self.selected_student_id)
                if success:
                    messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                    self.load_students()
                    self.selected_student_id = None
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el estudiante")
                    self.selected_student_id = None  # También limpiar en caso de error
            except Exception:
                messagebox.showerror("Error", "Ocurrió un error al eliminar el estudiante. Por favor, intente nuevamente.")
                self.selected_student_id = None  # Limpiar también en caso de excepción
    
    def show_student_form(self, student: Optional[Dict[str, Any]] = None):
        """Muestra el formulario de estudiante"""
        form_window = tk.Toplevel(self.parent)
        form_window.title("Nuevo Estudiante" if not student else "Editar Estudiante")
        form_window.geometry("500x400")
        form_window.resizable(False, False)
        form_window.transient(self.parent)
        form_window.grab_set()
        
        # Centrar ventana
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (form_window.winfo_screenheight() // 2) - (400 // 2)
        form_window.geometry(f'500x400+{x}+{y}')
        
        # Formulario
        self.create_student_form_content(form_window, student)
    
    def create_student_form_content(self, parent: tk.Toplevel, student: Optional[Dict[str, Any]]):
        """Crea el contenido del formulario de estudiante"""
        # Frame principal
        main_frame = tk.Frame(parent, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Campos del formulario
        fields = {}
        
        # Nombre
        tk.Label(main_frame, text="Nombre *:", font=('Segoe UI', 10), bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        fields['first_name'] = tk.Entry(main_frame, font=('Segoe UI', 10), width=30)
        fields['first_name'].grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Apellido
        tk.Label(main_frame, text="Apellido *:", font=('Segoe UI', 10), bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        fields['last_name'] = tk.Entry(main_frame, font=('Segoe UI', 10), width=30)
        fields['last_name'].grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Aula
        tk.Label(main_frame, text="Aula:", font=('Segoe UI', 10), bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
        
        # Obtener aulas disponibles
        try:
            classrooms = classroom_repo.get_all()
            classroom_names = [f"{c['id']} - {c['name']}" for c in classrooms]
        except Exception:
            classroom_names = ["Error cargando aulas"]
        
        fields['classroom_id'] = ttk.Combobox(main_frame, values=classroom_names, font=('Segoe UI', 10), width=28)
        if classroom_names == ["Error cargando aulas"]:
            fields['classroom_id'].configure(state='disabled')
        fields['classroom_id'].grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Estado
        tk.Label(main_frame, text="Estado:", font=('Segoe UI', 10), bg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=5)
        fields['enrollment_status'] = ttk.Combobox(main_frame, values=['activo', 'retirado', 'graduado'], font=('Segoe UI', 10), width=28)
        fields['enrollment_status'].grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Tutor
        tk.Label(main_frame, text="Tutor:", font=('Segoe UI', 10), bg='#ecf0f1').grid(row=4, column=0, sticky='w', pady=5)
        fields['tutor_name'] = tk.Entry(main_frame, font=('Segoe UI', 10), width=30)
        fields['tutor_name'].grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Cargar datos si es edición
        if student:
            fields['first_name'].insert(0, student['first_name'])
            fields['last_name'].insert(0, student['last_name'])
            if student.get('classroom_id'):
                classroom = classroom_repo.get_by_id(student['classroom_id'])
                if classroom:
                    fields['classroom_id'].set(f"{classroom['id']} - {classroom['name']}")
            fields['enrollment_status'].set(student['enrollment_status'])
            if student.get('tutor_name'):
                fields['tutor_name'].insert(0, student['tutor_name'])
        else:
            # Valores por defecto
            fields['enrollment_status'].set('activo')
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Guardar",
            font=('Segoe UI', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=lambda: self.save_student(parent, fields, student)
        )
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancelar",
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=parent.destroy
        )
        cancel_btn.pack(side='left', padx=5)
    
    def save_student(self, parent: tk.Toplevel, fields: Dict, student: Optional[Dict[str, Any]]):
        """Guarda los datos del estudiante"""
        try:
            # Validar campos obligatorios
            first_name = fields['first_name'].get().strip()
            last_name = fields['last_name'].get().strip()
            tutor_name = fields['tutor_name'].get().strip()
            
            if not first_name or not last_name:
                messagebox.showerror("Error de Validación", 
                                  "Nombre y apellido son obligatorios")
                return
            
            if len(first_name) > 100:
                messagebox.showerror("Error de Validación", "El nombre no puede exceder 100 caracteres")
                return
            
            if len(last_name) > 100:
                messagebox.showerror("Error de Validación", "El apellido no puede exceder 100 caracteres")
                return
            
            if len(tutor_name) > 100:
                messagebox.showerror("Error de Validación", "El nombre del tutor no puede exceder 100 caracteres")
                return
            
            # Preparar datos
            student_data = {
                'first_name': first_name,
                'last_name': last_name,
                'tutor_name': fields['tutor_name'].get().strip(),
                'enrollment_status': fields['enrollment_status'].get()
            }
            
            # Procesar aula
            classroom_text = fields['classroom_id'].get()
            if classroom_text and ' - ' in classroom_text:
                try:
                    classroom_id = int(classroom_text.split(' - ')[0])
                    student_data['classroom_id'] = classroom_id
                except ValueError:
                    messagebox.showerror("Error de Validación", "El formato del aula seleccionada es inválido")
                    return
            
            # Guardar
            if student:
                # Actualizar
                success = self.student_service.update_student(student['id'], student_data)
                if success:
                    messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
                    parent.destroy()
                    self.load_students()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el estudiante")
            else:
                # Crear
                student_id = self.student_service.create_student(student_data)
                if student_id:
                    messagebox.showinfo("Éxito", "Estudiante creado correctamente")
                    parent.destroy()
                    self.load_students()
                else:
                    messagebox.showerror("Error", "No se pudo crear el estudiante")
        
        except Exception:
            messagebox.showerror("Error", "Ocurrió un error al guardar el estudiante. Por favor, intente nuevamente.")
    
    def show_help(self):
        """Muestra ayuda"""
        help_text = """
        Gestión de Estudiantes - Ayuda
        
        • Nuevo Estudiante: Crea un nuevo registro de estudiante
        • Editar: Modifica los datos del estudiante seleccionado
        • Eliminar: Cambia el estado a 'retirado'
        • Buscar: Filtra por nombre, apellido o tutor
        
        Campos obligatorios: Nombre y Apellido
        """
        messagebox.showinfo("Ayuda", help_text)
    
    def darken_color(self, color: str) -> str:
        """Oscurece un color para efecto hover"""
        # Simple implementación - en producción usar librería de colores
        color_map = {
            '#27ae60': '#229954',
            '#3498db': '#2980b9',
            '#e74c3c': '#c0392b',
            '#95a5a6': '#7f8c8d'
        }
        return color_map.get(color, color)
