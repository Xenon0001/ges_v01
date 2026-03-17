"""
Reports View - Módulo de generación de reportes PDF
Interfaz gráfica para generar y descargar reportes académicos y financieros
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
        
        # Variables para controles
        self.selected_student = tk.StringVar()
        self.selected_classroom = tk.StringVar()
        self.selected_year = tk.StringVar()
        self.selected_trimester = tk.StringVar()
        self.overdue_only = tk.BooleanVar(value=True)
        
        # Configurar año actual por defecto (2 años atrás para datos existentes)
        current_year = datetime.now().year
        self.selected_year.set(str(current_year - 2))
        
        # Crear interfaz principal
        self.setup_ui()
        
        # Cargar datos iniciales
        self.load_initial_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        # Frame principal
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="MÓDULO DE REPORTES", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear pestañas
        self.create_academic_reports_tab()
        self.create_financial_reports_tab()
        self.create_classroom_reports_tab()
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para generar reportes")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
    def create_academic_reports_tab(self):
        """Crea pestaña de reportes académicos"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="Reportes Académicos")
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(tab_frame, text="Parámetros del Reporte", padding="10")
        controls_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Selección de estudiante
        ttk.Label(controls_frame, text="Estudiante:").pack(anchor=tk.W, pady=5)
        self.student_combo = ttk.Combobox(controls_frame, textvariable=self.selected_student, 
                                         state="readonly", width=30)
        self.student_combo.pack(padx=5, pady=5, fill=tk.X)
        
        # Año académico
        ttk.Label(controls_frame, text="Año Académico:").pack(anchor=tk.W, pady=5)
        self.year_combo = ttk.Combobox(controls_frame, textvariable=self.selected_year, 
                                       state="readonly", width=10)
        self.year_combo.pack(padx=5, pady=5, anchor=tk.W)
        
        # Trimestre
        ttk.Label(controls_frame, text="Trimestre:").pack(anchor=tk.W, pady=5)
        trimester_frame = ttk.Frame(controls_frame)
        trimester_frame.pack(padx=5, pady=5, anchor=tk.W)
        
        self.trimester_combo = ttk.Combobox(trimester_frame, textvariable=self.selected_trimester,
                                           state="readonly", width=8)
        self.trimester_combo['values'] = ['Todos', '1', '2', '3']
        self.trimester_combo.set('Todos')
        self.trimester_combo.pack(side=tk.LEFT)
        
        # Botón de generación
        generate_btn = ttk.Button(controls_frame, text="Generar Reporte de Notas",
                                 command=self.generate_student_report)
        generate_btn.pack(pady=20)
        
        # Información del reporte
        info_frame = ttk.LabelFrame(tab_frame, text="Información del Reporte", padding="10")
        info_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        info_text = """Este reporte incluye:
• Datos personales del estudiante
• Calificaciones por materia
• Promedio general y estado académico
• Resumen de materias aprobadas/reprobadas

El PDF se generará y abrirá automáticamente."""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
        
        # Configurar pesos
        tab_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_financial_reports_tab(self):
        """Crea pestaña de reportes financieros"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="Reportes Financieros")
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(tab_frame, text="Parámetros del Reporte", padding="10")
        controls_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Opciones de reporte
        ttk.Label(controls_frame, text="Tipo de Reporte:").pack(anchor=tk.W, pady=5)
        
        # Radio buttons para tipo de reporte
        self.report_type = tk.StringVar(value="overdue")
        overdue_radio = ttk.Radiobutton(controls_frame, text="Solo pagos vencidos",
                                       variable=self.report_type, value="overdue")
        overdue_radio.pack(anchor=tk.W, pady=5)
        
        pending_radio = ttk.Radiobutton(controls_frame, text="Todos los pagos pendientes",
                                       variable=self.report_type, value="pending")
        pending_radio.pack(anchor=tk.W, pady=5)
        
        # Botón de generación
        generate_btn = ttk.Button(controls_frame, text="Generar Reporte de Morosidad",
                                 command=self.generate_delinquency_report)
        generate_btn.pack(pady=20)
        
        # Información del reporte
        info_frame = ttk.LabelFrame(tab_frame, text="Información del Reporte", padding="10")
        info_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        info_text = """Este reporte incluye:
• Resumen ejecutivo de pagos
• Lista detallada por estudiante/tutor
• Estadísticas de morosidad
• Montos totales y tasas de cobro
• Identificación de casos críticos

El PDF se generará y abrirá automáticamente."""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
        
        # Configurar pesos
        tab_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_classroom_reports_tab(self):
        """Crea pestaña de reportes por aula"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="Reportes por Aula")
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(tab_frame, text="Parámetros del Reporte", padding="10")
        controls_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Selección de aula
        ttk.Label(controls_frame, text="Aula:").pack(anchor=tk.W, pady=5)
        self.classroom_combo = ttk.Combobox(controls_frame, textvariable=self.selected_classroom,
                                            state="readonly", width=30)
        self.classroom_combo.pack(padx=5, pady=5, fill=tk.X)
        
        # Año académico
        ttk.Label(controls_frame, text="Año Académico:").pack(anchor=tk.W, pady=5)
        self.classroom_year_combo = ttk.Combobox(controls_frame, textvariable=self.selected_year,
                                                 state="readonly", width=10)
        self.classroom_year_combo.pack(padx=5, pady=5, anchor=tk.W)
        
        # Trimestre
        ttk.Label(controls_frame, text="Trimestre:").pack(anchor=tk.W, pady=5)
        classroom_trimester_frame = ttk.Frame(controls_frame)
        classroom_trimester_frame.pack(padx=5, pady=5, anchor=tk.W)
        
        self.classroom_trimester_combo = ttk.Combobox(classroom_trimester_frame, 
                                                     textvariable=self.selected_trimester,
                                                     state="readonly", width=8)
        self.classroom_trimester_combo['values'] = ['Todos', '1', '2', '3']
        self.classroom_trimester_combo.set('Todos')
        self.classroom_trimester_combo.pack(side=tk.LEFT)
        
        # Botón de generación
        generate_btn = ttk.Button(controls_frame, text="Generar Reporte de Rendimiento",
                                 command=self.generate_classroom_report)
        generate_btn.pack(pady=20)
        
        # Información del reporte
        info_frame = ttk.LabelFrame(tab_frame, text="Información del Reporte", padding="10")
        info_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        info_text = """Este reporte incluye:
• Información general del aula
• Estadísticas de rendimiento
• Rendimiento por materia
• Lista de estudiantes en riesgo
• Recomendaciones pedagógicas

El PDF se generará y abrirá automáticamente."""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
        
        # Configurar pesos
        tab_frame.pack(fill=tk.BOTH, expand=True)
    
    def load_initial_data(self):
        """Carga datos iniciales en los comboboxes"""
        try:
            # Cargar estudiantes
            students = student_repo.get_all()
            student_list = [f"{s['id']} - {s.get('first_name', '')} {s.get('last_name', '')}" 
                            for s in students if s.get('enrollment_status') == 'activo']
            self.student_combo['values'] = student_list
            
            if student_list:
                self.student_combo.current(0)
                self.update_selected_student()
            
            # Cargar aulas
            classrooms = classroom_repo.get_all()
            classroom_list = [f"{c['id']} - {c['name']}" for c in classrooms]
            self.classroom_combo['values'] = classroom_list
            
            if classroom_list:
                self.classroom_combo.current(0)
                self.update_selected_classroom()
            
            # Cargar años (últimos 5 años + actual)
            current_year = datetime.now().year
            years = [str(year) for year in range(current_year - 5, current_year + 1)]
            self.year_combo['values'] = years
            self.classroom_year_combo['values'] = years
            
            # Vincular eventos
            self.student_combo.bind('<<ComboboxSelected>>', lambda e: self.update_selected_student())
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
            
            # Actualizar estado
            self.status_var.set("Generando reporte académico...")
            self.parent.update()
            
            # Generar reporte
            filename = self.report_service.generate_student_academic_report(
                student_id, academic_year, trimester
            )
            
            # Abrir PDF automáticamente
            if os.path.exists(filename):
                os.startfile(filename)
                self.status_var.set(f"Reporte generado: {os.path.basename(filename)}")
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{filename}")
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte.")
                self.status_var.set("Error al generar reporte")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error en parámetros")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            self.status_var.set("Error al generar reporte")
    
    def generate_delinquency_report(self):
        """Genera reporte de morosidad"""
        try:
            # Determinar tipo de reporte
            overdue_only = self.report_type.get() == "overdue"
            
            # Actualizar estado
            self.status_var.set("Generando reporte de morosidad...")
            self.parent.update()
            
            # Generar reporte
            filename = self.report_service.generate_delinquency_report(overdue_only)
            
            # Abrir PDF automáticamente
            if os.path.exists(filename):
                os.startfile(filename)
                self.status_var.set(f"Reporte generado: {os.path.basename(filename)}")
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{filename}")
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte.")
                self.status_var.set("Error al generar reporte")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            self.status_var.set("Error al generar reporte")
    
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
            
            # Actualizar estado
            self.status_var.set("Generando reporte de aula...")
            self.parent.update()
            
            # Generar reporte
            filename = self.report_service.generate_classroom_performance_report(
                classroom_id, academic_year, trimester
            )
            
            # Abrir PDF automáticamente
            if os.path.exists(filename):
                os.startfile(filename)
                self.status_var.set(f"Reporte generado: {os.path.basename(filename)}")
                messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{filename}")
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte.")
                self.status_var.set("Error al generar reporte")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error en parámetros")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            self.status_var.set("Error al generar reporte")
