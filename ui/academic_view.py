"""
Academic View - Gestión académica completa
Interfaz profesional para análisis y gestión académica
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Optional
from datetime import datetime

from services.academic_service import AcademicService
from database.repository import subject_repo, classroom_repo, student_repo


class AcademicView:
    """Vista de gestión académica"""
    
    def __init__(self, parent: tk.Frame, config: Dict[str, Any], 
                 academic_service=None):
        self.parent = parent
        self.config = config
        self.academic_service = academic_service if academic_service else AcademicService()
        
        # Estado
        self.current_section = "materias"
        self.academic_year = self.config.get('academic_year', 2024)
        
        # Crear UI
        self.create_widgets()
        
        # Cargar sección inicial
        self.show_section("materias")
    
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
            text="📚 Gestión Académica",
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
            ("📊 Materias", "materias", '#3498db'),
            ("🏫 Aulas", "aulas", '#27ae60'),
            ("👨‍🎓 Estudiantes", "estudiantes", '#e67e22'),
            ("⚠️ Alertas", "alertas", '#e74c3c')
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
        
        canvas.create_window((0, 0), window=self.content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
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
        if section_id == "materias":
            self.show_materias_section()
        elif section_id == "aulas":
            self.show_aulas_section()
        elif section_id == "estudiantes":
            self.show_estudiantes_section()
        elif section_id == "alertas":
            self.show_alertas_section()
    
    def update_nav_buttons(self, active_section: str):
        """Actualiza los colores de los botones de navegación"""
        colors = {
            "materias": '#3498db',
            "aulas": '#27ae60',
            "estudiantes": '#e67e22',
            "alertas": '#e74c3c'
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
        Gestión Académica - Ayuda
        
        📊 Materias: Análisis de rendimiento por materia
        🏫 Aulas: Rendimiento académico por aula
        👨‍🎓 Estudiantes: Gestión de calificaciones individuales
        ⚠️ Alertas: Alertas académicas activas
        
        Use los botones superiores para navegar entre secciones.
        """
        messagebox.showinfo("Ayuda", help_text)
    
    # Métodos placeholder para cada sección (se implementarán luego)
    def show_materias_section(self):
        """Muestra la sección de análisis por materia"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y filtros
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="📊 Análisis por Materia",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Filtro por trimestre
        filter_frame = tk.Frame(title_frame, bg='white')
        filter_frame.pack(side='right')
        
        tk.Label(filter_frame, text="Trimestre:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.trimester_var = tk.StringVar(value="Todos")
        trimester_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.trimester_var,
            values=["Todos", "1", "2", "3"],
            font=('Segoe UI', 10),
            width=10,
            state='readonly'
        )
        trimester_combo.pack(side='left')
        trimester_combo.bind('<<ComboboxSelected>>', lambda e: self.load_materias_data())
        
        # Tarjetas de métricas
        self.create_materias_metric_cards()
        
        # Tabla de materias
        self.create_materias_table()
        
        # Cargar datos iniciales
        self.load_materias_data()
    
    def create_materias_metric_cards(self):
        """Crea las tarjetas de métricas para materias"""
        cards_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        cards_frame.pack(fill='x', pady=(0, 10))
        
        # Tarjeta: Mejor materia
        self.best_subject_card = self.create_metric_card(
            cards_frame,
            "🏆 Mejor Materia",
            "Sin datos",
            "#27ae60",
            0
        )
        
        # Tarjeta: Peor materia
        self.worst_subject_card = self.create_metric_card(
            cards_frame,
            "⚠️ Peor Materia", 
            "Sin datos",
            "#e74c3c",
            1
        )
        
        # Tarjeta: Promedio general
        self.avg_general_card = self.create_metric_card(
            cards_frame,
            "📈 Promedio General",
            "0.0",
            "#3498db",
            2
        )
    
    def create_metric_card(self, parent, title: str, value: str, color: str, column: int):
        """Crea una tarjeta de métrica individual"""
        card = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        
        # Contenido de la tarjeta
        content_frame = tk.Frame(card, bg='white')
        content_frame.pack(pady=15, padx=15, fill='both', expand=True)
        
        # Título
        title_label = tk.Label(
            content_frame,
            text=title,
            font=('Segoe UI', 11),
            fg='#7f8c8d',
            bg='white'
        )
        title_label.pack(anchor='w', pady=(0, 8))
        
        # Valor
        value_label = tk.Label(
            content_frame,
            text=value,
            font=('Segoe UI', 18, 'bold'),
            fg=color,
            bg='white'
        )
        value_label.pack(anchor='w')
        
        return value_label
    
    def create_materias_table(self):
        """Crea la tabla de materias"""
        # Frame de la tabla
        table_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview (tabla)
        self.materias_tree = ttk.Treeview(
            table_frame,
            columns=('Materia', 'Promedio', 'TasaAprobacion', 'EstudiantesRiesgo'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar columnas
        self.materias_tree.heading('Materia', text='Materia')
        self.materias_tree.heading('Promedio', text='Promedio')
        self.materias_tree.heading('TasaAprobacion', text='Tasa Aprobación %')
        self.materias_tree.heading('EstudiantesRiesgo', text='Estudiantes en Riesgo')
        
        # Configurar anchos
        self.materias_tree.column('Materia', width=200, minwidth=150)
        self.materias_tree.column('Promedio', width=100, minwidth=80)
        self.materias_tree.column('TasaAprobacion', width=150, minwidth=120)
        self.materias_tree.column('EstudiantesRiesgo', width=180, minwidth=150)
        
        # Empaquetar con pack
        self.materias_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
    
    
    def create_aulas_table(self):
        """Crea la tabla de estudiantes del aula"""
        table_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        info_label = tk.Label(
            table_frame,
            text="📋 Mostrando: estudiantes en riesgo y mejores desempeños",
            font=('Segoe UI', 10, 'italic'),
            fg='#7f8c8d',
            bg='white'
        )
        info_label.pack(pady=(10, 5))
        
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        self.aulas_tree = ttk.Treeview(
            table_frame,
            columns=('Nombre', 'Apellido', 'Promedio', 'EstadoAcademico'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        self.aulas_tree.heading('Nombre', text='Nombre')
        self.aulas_tree.heading('Apellido', text='Apellido')
        self.aulas_tree.heading('Promedio', text='Promedio')
        self.aulas_tree.heading('EstadoAcademico', text='Estado Académico')
        
        self.aulas_tree.column('Nombre', width=150, minwidth=120)
        self.aulas_tree.column('Apellido', width=150, minwidth=120)
        self.aulas_tree.column('Promedio', width=100, minwidth=80)
        self.aulas_tree.column('EstadoAcademico', width=180, minwidth=150)
        
        self.aulas_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
    
    
    def load_materias_data(self):
        """Carga los datos de materias"""
        try:
            # Obtener filtro de trimestre
            trimestre_filter = self.trimester_var.get()
            
            # Obtener todas las materias
            subjects = subject_repo.get_all()
            if not subjects:
                self.show_no_data_message("No hay materias registradas")
                return
            
            # Analizar cada materia
            subjects_data = []
            for subject in subjects:
                try:
                    analysis = self.academic_service.get_subject_performance_analysis(
                        subject['id'], self.academic_year
                    )
                    
                    if 'error' not in analysis and 'annual_performance' in analysis:
                        performance = analysis['annual_performance']
                        
                        # Filtrar por trimestre si es necesario
                        if trimestre_filter != "Todos":
                            trimester_num = int(trimestre_filter)
                            trimester_key = f'trimester_{trimester_num}'
                            if trimester_key in analysis.get('trimester_breakdown', {}):
                                performance = analysis['trimester_breakdown'][trimester_key]
                            else:
                                continue  # No hay datos para este trimestre
                        
                        subjects_data.append({
                            'name': subject['name'],
                            'average': performance.get('average', 0),
                            'pass_rate': performance.get('pass_rate', 0),
                            'students_at_risk': performance.get('students_at_risk', 0),
                            'student_count': performance.get('student_count', 0)
                        })
                except Exception as e:
                    print(f"Error analizando materia {subject['name']}: {e}")
                    continue
            
            if not subjects_data:
                self.show_no_data_message("No hay calificaciones registradas para este período")
                return
            
            # Actualizar tabla
            self.populate_materias_table(subjects_data)
            
            # Actualizar métricas
            self.update_materias_metrics(subjects_data)
            
        except Exception as e:
            print(f"Error cargando datos de materias: {e}")
            self.show_no_data_message("Error al cargar los datos. Por favor, intente nuevamente.")
    
    
    def populate_materias_table(self, subjects_data):
        """Llena la tabla con datos de materias"""
        # Limpiar tabla
        for item in self.materias_tree.get_children():
            self.materias_tree.delete(item)
        
        # Agregar materias
        for subject in subjects_data:
            self.materias_tree.insert('', 'end', values=(
                subject['name'],
                f"{subject['average']:.2f}" if subject['average'] else "N/A",
                f"{subject['pass_rate']*100:.1f}%" if subject['pass_rate'] else "0%",
                f"{subject['students_at_risk']} ({subject['student_count']})"
            ))
    
    def update_materias_metrics(self, subjects_data):
        """Actualiza las tarjetas de métricas"""
        if not subjects_data:
            return
        
        # Mejor materia (mayor promedio)
        best_subject = max(subjects_data, key=lambda x: x['average'] if x['average'] else 0)
        self.best_subject_card.config(text=f"{best_subject['name']} ({best_subject['average']:.2f})")
        
        # Peor materia (menor promedio)
        worst_subject = min(subjects_data, key=lambda x: x['average'] if x['average'] else 0)
        self.worst_subject_card.config(text=f"{worst_subject['name']} ({worst_subject['average']:.2f})")
        
        # Promedio general
        valid_averages = [s['average'] for s in subjects_data if s['average'] is not None]
        if valid_averages:
            general_avg = sum(valid_averages) / len(valid_averages)
            self.avg_general_card.config(text=f"{general_avg:.2f}")
    
    def show_no_data_message(self, message: str):
        """Muestra un mensaje cuando no hay datos"""
        # Limpiar solo la tabla
        if hasattr(self, 'materias_tree'):
            for item in self.materias_tree.get_children():
                self.materias_tree.delete(item)
        
        # Insertar fila de mensaje en la tabla
        if hasattr(self, 'materias_tree'):
            self.materias_tree.insert('', 'end', values=(
                message, '', '', ''
            ))
    
    def show_aulas_section(self):
        """Muestra la sección de rendimiento por aula"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y filtros
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🏫 Rendimiento por Aula",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Filtros
        filter_frame = tk.Frame(title_frame, bg='white')
        filter_frame.pack(side='right')
        
        # Selector de aula
        tk.Label(filter_frame, text="Aula:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.classroom_var = tk.StringVar()
        self.classroom_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.classroom_var,
            font=('Segoe UI', 10),
            width=20,
            state='readonly'
        )
        self.classroom_combo.pack(side='left', padx=(0, 15))
        self.classroom_combo.bind('<<ComboboxSelected>>', lambda e: self.load_aulas_data())
        
        # Filtro por trimestre
        tk.Label(filter_frame, text="Trimestre:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.aulas_trimester_var = tk.StringVar(value="Todos")
        trimester_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.aulas_trimester_var,
            values=["Todos", "1", "2", "3"],
            font=('Segoe UI', 10),
            width=10,
            state='readonly'
        )
        trimester_combo.pack(side='left')
        trimester_combo.bind('<<ComboboxSelected>>', lambda e: self.load_aulas_data())
        
        # Cargar aulas disponibles
        self.load_classrooms()
        
        # Tarjetas de métricas
        self.create_aulas_metric_cards()
        
        # Tabla de estudiantes del aula
        self.create_aulas_table()
        
        # Cargar datos iniciales si hay aula seleccionada
        if self.classroom_var.get():
            self.load_aulas_data()
    
    def load_classrooms(self):
        """Carga las aulas disponibles en el dropdown"""
        try:
            classrooms = classroom_repo.get_all()
            if not classrooms:
                self.show_no_data_message_aulas("No hay aulas registradas en el sistema")
                return
            
            classroom_options = [f"{c['id']} - {c['name']}" for c in classrooms]
            self.classroom_combo['values'] = classroom_options
            
            # Seleccionar primera aula por defecto
            if classroom_options:
                self.classroom_var.set(classroom_options[0])
                self.current_classrooms = classrooms
            else:
                self.current_classrooms = []
                
        except Exception as e:
            print(f"Error cargando aulas: {e}")
            self.show_no_data_message_aulas("Error al cargar las aulas")
    
    def create_aulas_metric_cards(self):
        """Crea las tarjetas de métricas para aulas"""
        cards_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        cards_frame.pack(fill='x', pady=(0, 10))
        
        # Tarjeta: Total Estudiantes
        self.total_students_card = self.create_metric_card(
            cards_frame,
            "👥 Total Estudiantes",
            "0",
            "#3498db",
            0
        )
        
        # Tarjeta: Promedio del Aula
        self.classroom_avg_card = self.create_metric_card(
            cards_frame,
            "📈 Promedio del Aula", 
            "0.0",
            "#27ae60",
            1
        )
        
        # Tarjeta: Estudiantes en Riesgo
        self.at_risk_card = self.create_metric_card(
            cards_frame,
            "⚠️ Estudiantes en Riesgo",
            "0",
            "#e74c3c",
            2
        )
    
    def load_aulas_data(self):
        """Carga los datos del aula seleccionada"""
        try:
            # Validar que hay aula seleccionada
            if not self.classroom_var.get():
                self.show_no_data_message_aulas("Por favor seleccione un aula")
                return
            
            # Extraer ID del aula seleccionada
            classroom_text = self.classroom_var.get()
            if ' - ' not in classroom_text:
                self.show_no_data_message_aulas("Formato de aula inválido")
                return
            
            classroom_id = int(classroom_text.split(' - ')[0])
            
            # Obtener filtro de trimestre
            trimestre_filter = self.aulas_trimester_var.get()
            trimester_param = None if trimestre_filter == "Todos" else int(trimestre_filter)
            
            # Obtener datos del aula
            classroom_data = self.academic_service.get_classroom_academic_summary(
                classroom_id, self.academic_year, trimester_param
            )
            
            if 'error' in classroom_data:
                self.show_no_data_message_aulas(classroom_data['error'])
                return
            
            # Actualizar tabla
            self.populate_aulas_table(classroom_data)
            
            # Actualizar métricas
            self.update_aulas_metrics(classroom_data)
            
        except ValueError:
            self.show_no_data_message_aulas("Error en el formato del aula seleccionada")
        except Exception as e:
            print(f"Error cargando datos del aula: {e}")
            self.show_no_data_message_aulas("Error al cargar los datos del aula. Por favor, intente nuevamente.")
    
    def populate_aulas_table(self, classroom_data):
        """Llena la tabla con datos de estudiantes del aula"""
        # Limpiar tabla
        for item in self.aulas_tree.get_children():
            self.aulas_tree.delete(item)
        
        # Obtener lista de estudiantes
        students_at_risk = classroom_data.get('students_at_risk', [])
        top_performers = classroom_data.get('top_performers', [])
        
        # Combinar todos los estudiantes mencionados
        all_students = []
        
        # Agregar estudiantes en riesgo
        for student_data in students_at_risk:
            student_info = student_data.get('student_info', {})
            all_students.append({
                'name': student_info.get('first_name', ''),
                'last_name': student_info.get('last_name', ''),
                'average': student_data.get('average', 0),
                'status': 'Riesgo'
            })
        
        # Agregar mejores desempeños
        for student_data in top_performers:
            student_info = student_data.get('student_info', {})
            all_students.append({
                'name': student_info.get('first_name', ''),
                'last_name': student_info.get('last_name', ''),
                'average': student_data.get('average', 0),
                'status': 'Excelente'
            })
        
        # Ordenar por promedio descendente
        all_students.sort(key=lambda x: x['average'] if x['average'] else 0, reverse=True)
        
        # Agregar estudiantes a la tabla
        for student in all_students:
            status_text = student['status']
            
            if student['status'] == 'Riesgo':
                status_text = f"⚠️ {student['status']}"
            elif student['status'] == 'Excelente':
                status_text = f"🏆 {student['status']}"
            
            self.aulas_tree.insert('', 'end', values=(
                student['name'],
                student['last_name'],
                f"{student['average']:.2f}" if student['average'] else "N/A",
                status_text
            ))
    
    def update_aulas_metrics(self, classroom_data):
        """Actualiza las tarjetas de métricas del aula"""
        # Total estudiantes
        total_students = classroom_data.get('total_students', 0)
        self.total_students_card.config(text=str(total_students))
        
        # Promedio del aula
        performance_metrics = classroom_data.get('performance_metrics', {})
        classroom_avg = performance_metrics.get('classroom_average', 0)
        self.classroom_avg_card.config(text=f"{classroom_avg:.2f}" if classroom_avg else "N/A")
        
        # Estudiantes en riesgo
        students_at_risk = performance_metrics.get('students_at_risk', 0)
        self.at_risk_card.config(text=str(students_at_risk))
    
    def show_no_data_message_aulas(self, message: str):
        """Muestra un mensaje cuando no hay datos para aulas"""
        # Limpiar solo la tabla
        if hasattr(self, 'aulas_tree'):
            for item in self.aulas_tree.get_children():
                self.aulas_tree.delete(item)
        
        # Insertar fila de mensaje en la tabla
        if hasattr(self, 'aulas_tree'):
            self.aulas_tree.insert('', 'end', values=(
                message, '', '', ''
            ))
    
    def show_estudiantes_section(self):
        """Muestra la sección de calificaciones por estudiante"""
        placeholder = tk.Label(
            self.content_frame,
            text="👨‍🎓 Calificaciones por Estudiante - En implementación...",
            font=('Segoe UI', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        placeholder.pack(pady=50)
    
    def show_alertas_section(self):
        """Muestra la sección de alertas académicas"""
        placeholder = tk.Label(
            self.content_frame,
            text="⚠️ Alertas Académicas - En implementación...",
            font=('Segoe UI', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        placeholder.pack(pady=50)
