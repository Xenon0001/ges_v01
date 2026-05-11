"""
Reports View - Módulo de generación de reportes PDF
Interfaz profesional siguiendo el patrón de otros módulos
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from services.report_service import ReportService
from database.repository import student_repo, classroom_repo


class ReportsView:
    """Vista principal del módulo de reportes"""
    
    def __init__(self, parent, config=None, report_service=None):
        self.parent = parent
        self.config = config or {}
        self.report_service = report_service or ReportService()
        
        # Estado
        self.current_section = "notas"
        
        # Variables para controles
        self.selected_student = tk.StringVar()
        self.selected_classroom = tk.StringVar()
        self.selected_year = tk.StringVar()
        self.selected_trimester = tk.StringVar()
        self.overdue_only = tk.BooleanVar(value=True)
        
        # Configurar año actual por defecto (2 años atrás para datos existentes)
        current_year = datetime.now().year
        self.selected_year.set(str(current_year - 2))
        
        # Crear UI
        self.create_widgets()
        
        # Cargar sección inicial
        self.show_section("notas")
    
    def create_widgets(self):
        """Crea todos los widgets"""
        # Header
        self.create_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.parent, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Navegación de secciones
        self.create_section_navigation(main_container)
        
        # Contenido dinámico
        self.create_content_area(main_container)
    
    def create_header(self):
        """Crea el header de la vista"""
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="📊 Reportes",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        # Botones de acción
        right_frame = tk.Frame(header_frame, bg='#2c3e50')
        right_frame.pack(side='right', padx=20, pady=15)
        
        # Botón de ayuda
        help_btn = tk.Button(
            right_frame,
            text="❓",
            font=('Segoe UI', 12),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.show_help
        )
        help_btn.pack(side='left', padx=(0, 5))
        
        # Botón de refrescar
        refresh_btn = tk.Button(
            right_frame,
            text="🔄",
            font=('Segoe UI', 12),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.refresh_current_section
        )
        refresh_btn.pack(side='left')
    
    def create_section_navigation(self, parent):
        """Crea la navegación entre secciones"""
        nav_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        nav_frame.pack(fill='x', pady=(0, 10))
        
        # Contenedor de botones
        buttons_container = tk.Frame(nav_frame, bg='white')
        buttons_container.pack(pady=10, padx=20)
        
        # Botones de navegación
        self.nav_buttons = {}
        
        sections = [
            ("📚 Notas", "notas", '#3498db'),
            ("💰 Morosidad", "morosidad", '#e74c3c'),
            ("🏫 Rendimiento", "rendimiento", '#27ae60')
        ]
        
        for text, section_id, color in sections:
            btn = tk.Button(
                buttons_container,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                bg=color if section_id == self.current_section else '#95a5a6',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=lambda s=section_id: self.show_section(s),
                padx=15,
                pady=8
            )
            btn.pack(side='left', padx=5)
            self.nav_buttons[section_id] = btn
    
    def create_content_area(self, parent):
        """Crea el área de contenido dinámico"""
        # Frame scrollable para contenido
        canvas = tk.Canvas(parent, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.content_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        self.content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        self.content_canvas_window = canvas.create_window((0, 0), window=self.content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.bind('<Configure>', lambda e: (
            canvas.itemconfig(self.content_canvas_window, width=e.width),
            canvas.itemconfig(self.content_canvas_window, height=e.height)
        ))
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def show_section(self, section_id: str):
        """Muestra una sección específica"""
        self.current_section = section_id
        
        # Actualizar colores de botones
        self.update_nav_buttons(section_id)
        
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostrar contenido según sección
        if section_id == "notas":
            self.show_notas_section()
        elif section_id == "morosidad":
            self.show_morosidad_section()
        elif section_id == "rendimiento":
            self.show_rendimiento_section()
    
    def update_nav_buttons(self, active_section: str):
        """Actualiza los colores de los botones de navegación"""
        colors = {
            "notas": '#3498db',
            "morosidad": '#e74c3c',
            "rendimiento": '#27ae60'
        }
        
        for section_id, btn in self.nav_buttons.items():
            if section_id == active_section:
                btn.configure(bg=colors[section_id])
            else:
                btn.configure(bg='#95a5a6')
    
    def refresh_current_section(self):
        """Refresca la sección actual"""
        self.show_section(self.current_section)
    
    def show_help(self):
        """Muestra ayuda"""
        help_text = """
        Módulo de Reportes - Ayuda
        
        📚 Notas: Genera reportes académicos por estudiante
        💰 Morosidad: Genera reportes financieros de pagos vencidos
        🏫 Rendimiento: Genera reportes de rendimiento por aula
        
        Use los botones superiores para navegar entre secciones.
        """
        messagebox.showinfo("Ayuda", help_text)
    
    def show_notas_section(self):
        """Muestra la sección de reportes académicos"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y controles
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="📚 Reporte Académico por Estudiante",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Botón de generación
        generate_btn = tk.Button(
            title_frame,
            text="📄 Generar PDF",
            font=('Segoe UI', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.generate_student_report
        )
        generate_btn.pack(side='right')
        
        # Frame de controles
        controls_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Selección de estudiante
        student_frame = tk.Frame(controls_frame, bg='white')
        student_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(student_frame, text="Estudiante:", font=('Segoe UI', 10), bg='white').pack(anchor='w')
        self.student_combo = ttk.Combobox(student_frame, textvariable=self.selected_student, 
                                         state="readonly", width=30)
        self.student_combo.pack(fill='x', pady=5)
        
        # Frame de año y trimestre
        year_trimester_frame = tk.Frame(controls_frame, bg='white')
        year_trimester_frame.pack(fill='x', padx=20, pady=10)
        
        # Año académico
        tk.Label(year_trimester_frame, text="Año Académico:", font=('Segoe UI', 10), bg='white').pack(anchor='w')
        self.year_combo = ttk.Combobox(year_trimester_frame, textvariable=self.selected_year, 
                                       state="readonly", width=10)
        self.year_combo.pack(anchor='w', pady=5)
        
        # Trimestre
        tk.Label(year_trimester_frame, text="Trimestre:", font=('Segoe UI', 10), bg='white').pack(anchor='w', pady=(10, 0))
        self.trimester_combo = ttk.Combobox(year_trimester_frame, textvariable=self.selected_trimester,
                                           state="readonly", width=8)
        self.trimester_combo['values'] = ['Todos', '1', '2', '3']
        self.trimester_combo.set('Todos')
        self.trimester_combo.pack(anchor='w', pady=5)
        
        # Información del reporte
        info_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        info_frame.pack(fill='both', expand=True, pady=10)
        
        info_text = """Este reporte incluye:
• Datos personales del estudiante
• Calificaciones por materia
• Promedio general y estado académico
• Resumen de materias aprobadas/reprobadas

El PDF se generará y abrirá automáticamente."""
        
        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT, font=('Segoe UI', 10))
        info_label.pack(pady=20, padx=20)
        
        # Cargar datos iniciales
        self.load_students_data()
    
    def load_students_data(self):
        """Carga datos de estudiantes en el combo"""
        try:
            students = student_repo.get_all()
            student_list = [f"{s['id']} - {s.get('first_name', '')} {s.get('last_name', '')}" 
                            for s in students if s.get('enrollment_status') == 'activo']
            self.student_combo['values'] = student_list
            
            if student_list:
                self.student_combo.current(0)
                self.update_selected_student()
            
            # Cargar años (últimos 5 años + actual)
            current_year = datetime.now().year
            years = [str(year) for year in range(current_year - 5, current_year + 1)]
            self.year_combo['values'] = years
            
            # Vincular eventos
            self.student_combo.bind('<<ComboboxSelected>>', lambda e: self.update_selected_student())
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos iniciales: {str(e)}")
    
    def show_morosidad_section(self):
        """Muestra la sección de reportes de morosidad"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y botón
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="💰 Reporte de Morosidad",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        generate_btn = tk.Button(
            title_frame,
            text="📄 Generar PDF",
            font=('Segoe UI', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.generate_delinquency_report
        )
        generate_btn.pack(side='right')
        
        # Frame de controles
        controls_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Opciones de reporte
        options_frame = tk.Frame(controls_frame, bg='white')
        options_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(options_frame, text="Tipo de Reporte:", font=('Segoe UI', 10), bg='white').pack(anchor='w')
        
        # Radio buttons para tipo de reporte
        self.report_type = tk.StringVar(value="overdue")
        overdue_radio = tk.Radiobutton(options_frame, text="Solo pagos vencidos",
                                       variable=self.report_type, value="overdue", bg='white')
        overdue_radio.pack(anchor='w', pady=5)
        
        pending_radio = tk.Radiobutton(options_frame, text="Todos los pagos pendientes",
                                       variable=self.report_type, value="pending", bg='white')
        pending_radio.pack(anchor='w', pady=5)
        
        # Información del reporte
        info_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        info_frame.pack(fill='both', expand=True, pady=10)
        
        info_text = """Este reporte incluye:
• Resumen ejecutivo de pagos
• Lista detallada por estudiante/tutor
• Estadísticas de morosidad
• Montos totales y tasas de cobro
• Identificación de casos críticos

El PDF se generará y abrirá automáticamente."""
        
        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT, font=('Segoe UI', 10))
        info_label.pack(pady=20, padx=20)
    
    def show_rendimiento_section(self):
        """Muestra la sección de reportes de rendimiento"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y botón
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🏫 Reporte de Rendimiento por Aula",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        generate_btn = tk.Button(
            title_frame,
            text="📄 Generar PDF",
            font=('Segoe UI', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.generate_classroom_report
        )
        generate_btn.pack(side='right')
        
        # Frame de controles
        controls_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Selección de aula
        classroom_frame = tk.Frame(controls_frame, bg='white')
        classroom_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(classroom_frame, text="Aula:", font=('Segoe UI', 10), bg='white').pack(anchor='w')
        self.classroom_combo = ttk.Combobox(classroom_frame, textvariable=self.selected_classroom,
                                            state="readonly", width=30)
        self.classroom_combo.pack(fill='x', pady=5)
        
        # Frame de año y trimestre
        year_trimester_frame = tk.Frame(controls_frame, bg='white')
        year_trimester_frame.pack(fill='x', padx=20, pady=10)
        
        # Año académico
        tk.Label(year_trimester_frame, text="Año Académico:", font=('Segoe UI', 10), bg='white').pack(anchor='w')
        self.classroom_year_combo = ttk.Combobox(year_trimester_frame, textvariable=self.selected_year,
                                                 state="readonly", width=10)
        self.classroom_year_combo.pack(anchor='w', pady=5)
        
        # Trimestre
        tk.Label(year_trimester_frame, text="Trimestre:", font=('Segoe UI', 10), bg='white').pack(anchor='w', pady=(10, 0))
        self.classroom_trimester_combo = ttk.Combobox(year_trimester_frame, textvariable=self.selected_trimester,
                                                     state="readonly", width=8)
        self.classroom_trimester_combo['values'] = ['Todos', '1', '2', '3']
        self.classroom_trimester_combo.set('Todos')
        self.classroom_trimester_combo.pack(anchor='w', pady=5)
        
        # Información del reporte
        info_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        info_frame.pack(fill='both', expand=True, pady=10)
        
        info_text = """Este reporte incluye:
• Información general del aula
• Estadísticas de rendimiento
• Rendimiento por materia
• Lista de estudiantes en riesgo
• Recomendaciones pedagógicas

El PDF se generará y abrirá automáticamente."""
        
        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT, font=('Segoe UI', 10))
        info_label.pack(pady=20, padx=20)
        
        # Cargar datos iniciales
        self.load_classrooms_data()
    
    def load_classrooms_data(self):
        """Carga datos de aulas en el combo"""
        try:
            classrooms = classroom_repo.get_all()
            classroom_list = [f"{c['id']} - {c['name']}" for c in classrooms]
            self.classroom_combo['values'] = classroom_list
            
            if classroom_list:
                self.classroom_combo.current(0)
                self.update_selected_classroom()
            
            # Cargar años (últimos 5 años + actual)
            current_year = datetime.now().year
            years = [str(year) for year in range(current_year - 5, current_year + 1)]
            self.classroom_year_combo['values'] = years
            
            # Vincular eventos
            self.classroom_combo.bind('<<ComboboxSelected>>', lambda e: self.update_selected_classroom())
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos iniciales: {str(e)}")
    
    def update_selected_student(self):
        """Actualiza la variable del estudiante seleccionado"""
        selection = self.student_combo.get()
        if selection and ' - ' in selection:
            student_id = selection.split(' - ')[0]
            self.selected_student.set(student_id)
    
    def update_selected_classroom(self):
        """Actualiza la variable del aula seleccionada"""
        selection = self.classroom_combo.get()
        if selection and ' - ' in selection:
            classroom_id = selection.split(' - ')[0]
            self.selected_classroom.set(classroom_id)
    
    def generate_student_report(self):
        """Genera reporte académico de estudiante"""
        try:
            # Validar selección
            if not self.selected_student.get():
                messagebox.showwarning("Advertencia", "Por favor seleccione un estudiante.")
                return
            
            if not self.selected_year.get():
                messagebox.showwarning("Advertencia", "Por favor seleccione un año académico.")
                return
            
            # Obtener parámetros
            student_id = int(self.selected_student.get())
            academic_year = int(self.selected_year.get())
            
            # Determinar trimestre
            trimester = None
            if self.selected_trimester.get() != 'Todos':
                trimester = int(self.selected_trimester.get())
            
            # Generar reporte
            filename = self.report_service.generate_student_academic_report(
                student_id, academic_year, trimester
            )
            
            # Abrir PDF automáticamente
            if os.path.exists(filename):
                os.startfile(filename)
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{filename}")
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte.")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generate_delinquency_report(self):
        """Genera reporte de morosidad"""
        try:
            # Determinar tipo de reporte
            overdue_only = self.report_type.get() == "overdue"
            
            # Generar reporte
            filename = self.report_service.generate_delinquency_report(overdue_only)
            
            # Abrir PDF automáticamente
            if os.path.exists(filename):
                os.startfile(filename)
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{filename}")
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generate_classroom_report(self):
        """Genera reporte de rendimiento por aula"""
        try:
            # Validar selección
            if not self.selected_classroom.get():
                messagebox.showwarning("Advertencia", "Por favor seleccione un aula.")
                return
            
            if not self.selected_year.get():
                messagebox.showwarning("Advertencia", "Por favor seleccione un año académico.")
                return
            
            # Obtener parámetros
            classroom_id = int(self.selected_classroom.get())
            academic_year = int(self.selected_year.get())
            
            # Determinar trimestre
            trimester = None
            if self.selected_trimester.get() != 'Todos':
                trimester = int(self.selected_trimester.get())
            
            # Generar reporte
            filename = self.report_service.generate_classroom_performance_report(
                classroom_id, academic_year, trimester
            )
            
            # Abrir PDF automáticamente
            if os.path.exists(filename):
                os.startfile(filename)
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{filename}")
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte.")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
