"""
Finance View - Gestión financiera completa
Interfaz profesional para análisis y gestión de pagos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta

from services.finance_service import FinanceService
from database.repository import student_repo


class FinanceView:
    """Vista de gestión financiera"""
    
    def __init__(self, parent: tk.Frame, config: Dict[str, Any], 
                 finance_service=None):
        self.parent = parent
        self.config = config
        self.finance_service = finance_service if finance_service else FinanceService()
        
        # Estado
        self.current_section = "resumen"
        self.academic_year = self.config.get('academic_year', 2024)
        
        # Crear UI
        self.create_widgets()
        
        # Cargar sección inicial
        self.show_section("resumen")
    
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
            text="💰 Gestión Financiera",
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
            ("💰 Resumen", "resumen", '#27ae60'),
            ("👤 Por Estudiante", "estudiante", '#3498db'),
            ("⚠️ Morosidad", "morosidad", '#e74c3c'),
            ("👥 Por Tutor", "tutor", '#f39c12')
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
        if section_id == "resumen":
            self.show_resumen_section()
        elif section_id == "estudiante":
            self.show_estudiante_section()
        elif section_id == "morosidad":
            self.show_morosidad_section()
        elif section_id == "tutor":
            self.show_tutor_section()
    
    def update_nav_buttons(self, active_section: str):
        """Actualiza los colores de los botones de navegación"""
        colors = {
            "resumen": '#27ae60',
            "estudiante": '#3498db',
            "morosidad": '#e74c3c',
            "tutor": '#f39c12'
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
        Gestión Financiera - Ayuda
        
        💰 Resumen: Métricas generales del sistema financiero
        👤 Por Estudiante: Gestión de pagos individuales
        ⚠️ Morosidad: Control de pagos vencidos
        👥 Por Tutor: Resumen de pagos por tutor
        
        Use los botones superiores para navegar entre secciones.
        """
        messagebox.showinfo("Ayuda", help_text)
    
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
    
    def show_resumen_section(self):
        """Muestra la sección de resumen financiero"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="💰 Resumen Financiero",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Botón de actualizar
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 Actualizar",
            font=('Segoe UI', 10),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.load_resumen_data
        )
        refresh_btn.pack(side='right')
        
        # Tarjetas de métricas
        self.create_resumen_metric_cards()
        
        # Tabla de resumen
        self.create_resumen_table()
        
        # Cargar datos iniciales
        self.load_resumen_data()
    
    def create_resumen_metric_cards(self):
        """Crea las tarjetas de métricas para resumen"""
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
        
        # Tarjeta: Total Cobrado
        self.total_collected_card = self.create_metric_card(
            cards_frame,
            "� Total Cobrado",
            "0 FCFA",
            "#27ae60",
            1
        )
        
        # Tarjeta: Total Pendiente
        self.total_outstanding_card = self.create_metric_card(
            cards_frame,
            "⏳ Total Pendiente",
            "0 FCFA",
            "#e74c3c",
            2
        )
        
        # Tarjeta: Tasa de Cobro
        self.collection_rate_card = self.create_metric_card(
            cards_frame,
            "📈 Tasa de Cobro",
            "0.0%",
            "#f39c12",
            3
        )
    
    def create_resumen_table(self):
        """Crea la tabla de resumen financiero"""
        # Frame de la tabla
        table_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview (tabla)
        self.resumen_tree = ttk.Treeview(
            table_frame,
            columns=('Categoria', 'Monto', 'Cantidad', 'Porcentaje'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar columnas
        self.resumen_tree.heading('Categoria', text='Categoría')
        self.resumen_tree.heading('Monto', text='Monto')
        self.resumen_tree.heading('Cantidad', text='Cantidad')
        self.resumen_tree.heading('Porcentaje', text='Porcentaje')
        
        # Configurar anchos
        self.resumen_tree.column('Categoria', width=200, minwidth=150)
        self.resumen_tree.column('Monto', width=120, minwidth=100)
        self.resumen_tree.column('Cantidad', width=100, minwidth=80)
        self.resumen_tree.column('Porcentaje', width=120, minwidth=100)
        
        # Empaquetar
        self.resumen_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
    
    def load_resumen_data(self):
        """Carga los datos del resumen financiero"""
        try:
            # Obtener resumen de pagos
            summary = self.finance_service.get_payment_summary()
            
            # Actualizar tarjetas de métricas
            self.total_students_card.config(text=str(summary.total_students))
            self.total_collected_card.config(text=f"{summary.total_paid:.2f} FCFA")
            self.total_outstanding_card.config(text=f"{summary.total_outstanding:.2f} FCFA")
            self.collection_rate_card.config(text=f"{summary.collection_rate:.1f}%")
            
            # Actualizar tabla
            self.populate_resumen_table(summary)
            
        except Exception as e:
            print(f"Error cargando resumen financiero: {e}")
            self.show_resumen_error("Error al cargar los datos. Por favor, intente nuevamente.")
    
    def populate_resumen_table(self, summary):
        """Llena la tabla con datos del resumen"""
        # Limpiar tabla
        for item in self.resumen_tree.get_children():
            self.resumen_tree.delete(item)
        
        # Datos para la tabla
        table_data = [
            {
                'categoria': '💰 Total Debitado',
                'monto': f"{summary.total_due:.2f} FCFA",
                'cantidad': str(summary.total_students),
                'porcentaje': '100.0%'
            },
            {
                'categoria': '✅ Total Cobrado',
                'monto': f"{summary.total_paid:.2f} FCFA",
                'cantidad': f"{summary.total_students - summary.overdue_payments}",
                'porcentaje': f"{summary.collection_rate:.1f}%"
            },
            {
                'categoria': '⏳ Total Pendiente',
                'monto': f"{summary.total_outstanding:.2f} FCFA",
                'cantidad': str(summary.overdue_payments),
                'porcentaje': f"{100 - summary.collection_rate:.1f}%"
            },
            {
                'categoria': '⚠️ Pagos Vencidos',
                'monto': f"{summary.overdue_amount:.2f} FCFA",
                'cantidad': str(summary.overdue_payments),
                'porcentaje': f"{(summary.overdue_amount / summary.total_due * 100) if summary.total_due > 0 else 0:.1f}%"
            }
        ]
        
        # Agregar datos a la tabla
        for data in table_data:
            self.resumen_tree.insert('', 'end', values=(
                data['categoria'],
                data['monto'],
                data['cantidad'],
                data['porcentaje']
            ))
    
    def show_resumen_error(self, message: str):
        """Muestra un mensaje de error en resumen"""
        # Limpiar tabla
        for item in self.resumen_tree.get_children():
            self.resumen_tree.delete(item)
        
        # Insertar mensaje de error
        self.resumen_tree.insert('', 'end', values=(
            message, '', '', ''
        ))
    
    def show_estudiante_section(self):
        """Muestra la sección de pagos por estudiante"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y buscador
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="👤 Pagos por Estudiante",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Buscador de estudiantes
        search_frame = tk.Frame(title_frame, bg='white')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Buscar:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.student_search_var = tk.StringVar()
        self.student_search_entry = tk.Entry(
            search_frame,
            textvariable=self.student_search_var,
            font=('Segoe UI', 10),
            width=25
        )
        self.student_search_entry.pack(side='left', padx=(0, 10))
        self.student_search_entry.bind('<KeyRelease>', lambda e: self.filter_students())
        
        # Botón de búsqueda
        search_btn = tk.Button(
            search_frame,
            text="🔍",
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.filter_students
        )
        search_btn.pack(side='left')
        
        # Área de contenido
        content_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Frame izquierdo - lista de estudiantes
        left_frame = tk.Frame(content_frame, bg='#ecf0f1')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Tabla de estudiantes
        self.create_students_table(left_frame)
        
        # Frame derecho - información del estudiante seleccionado
        right_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1, width=400)
        right_frame.pack(side='right', fill='y', padx=(0, 20))
        right_frame.pack_propagate(False)
        
        # Información del estudiante
        self.create_student_info(right_frame)
        
        # Cargar lista de estudiantes
        self.load_students_list()
    
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
            columns=('Nombre', 'Apellido', 'Estado', 'Pendiente'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar columnas
        self.students_tree.heading('Nombre', text='Nombre')
        self.students_tree.heading('Apellido', text='Apellido')
        self.students_tree.heading('Estado', text='Estado Financiero')
        self.students_tree.heading('Pendiente', text='Pendiente')
        
        # Configurar anchos
        self.students_tree.column('Nombre', width=150, minwidth=120)
        self.students_tree.column('Apellido', width=150, minwidth=120)
        self.students_tree.column('Estado', width=150, minwidth=120)
        self.students_tree.column('Pendiente', width=100, minwidth=80)
        
        # Evento de selección
        self.students_tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # Empaquetar
        self.students_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
    
    def create_student_info(self, parent):
        """Crea el área de información del estudiante seleccionado"""
        # Canvas con scroll para el panel derecho
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        
        scroll_frame = tk.Frame(canvas, bg='white')
        scroll_frame.bind('<Configure>', 
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Todo el contenido existente va dentro de scroll_frame, no de parent
        # Título
        title_label = tk.Label(
            scroll_frame,
            text="Información del Estudiante",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=15, padx=15)
        
        # Frame de información
        info_frame = tk.Frame(scroll_frame, bg='white')
        info_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        # Nombre del estudiante
        self.student_name_label = tk.Label(
            info_frame,
            text="Seleccione un estudiante",
            font=('Segoe UI', 11, 'bold'),
            fg='#7f8c8d',
            bg='white'
        )
        self.student_name_label.pack(anchor='w', pady=(0, 5))
        
        # Tutor
        self.student_tutor_label = tk.Label(
            info_frame,
            text="",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='white'
        )
        self.student_tutor_label.pack(anchor='w', pady=(0, 5))
        
        # Estado financiero
        self.student_status_label = tk.Label(
            info_frame,
            text="",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        )
        self.student_status_label.pack(anchor='w', pady=(0, 10))
        
        # Separador
        separator = ttk.Separator(scroll_frame, orient='horizontal')
        separator.pack(fill='x', padx=15, pady=10)
        
        # Tabla de pagos del estudiante
        payments_label = tk.Label(
            scroll_frame,
            text="Pagos del Estudiante",
            font=('Segoe UI', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        payments_label.pack(pady=(10, 5), padx=15)
        
        # Frame para tabla de pagos
        payments_table_frame = tk.Frame(scroll_frame, bg='white')
        payments_table_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        # Treeview de pagos
        self.payments_tree = ttk.Treeview(
            payments_table_frame,
            columns=('MontoDue', 'MontoPaid', 'Estado', 'FechaVenc'),
            show='headings',
            height=8
        )
        
        # Configurar columnas
        self.payments_tree.heading('MontoDue', text='Debido')
        self.payments_tree.heading('MontoPaid', text='Pagado')
        self.payments_tree.heading('Estado', text='Estado')
        self.payments_tree.heading('FechaVenc', text='Vencimiento')
        
        # Configurar anchos
        self.payments_tree.column('MontoDue', width=80, minwidth=60)
        self.payments_tree.column('MontoPaid', width=80, minwidth=60)
        self.payments_tree.column('Estado', width=80, minwidth=60)
        self.payments_tree.column('FechaVenc', width=100, minwidth=80)
        
        self.payments_tree.pack(fill='both', expand=True)
        
        # Formulario de registro de pago
        self.create_payment_form(scroll_frame)
    
    def create_payment_form(self, parent):
        """Crea el formulario para registrar pagos"""
        # Separador
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill='x', padx=15, pady=10)
        
        # Título del formulario
        form_title = tk.Label(
            parent,
            text="Registrar Pago",
            font=('Segoe UI', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        form_title.pack(pady=(10, 5), padx=15)
        
        # Frame del formulario
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Selección de pago
        tk.Label(form_frame, text="Pago:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=2)
        self.payment_var = tk.StringVar()
        self.payment_combo = ttk.Combobox(
            form_frame,
            textvariable=self.payment_var,
            font=('Segoe UI', 10),
            width=20,
            state='readonly'
        )
        self.payment_combo.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Monto a pagar
        tk.Label(form_frame, text="Monto:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=2)
        self.payment_amount_var = tk.StringVar()
        payment_amount_entry = tk.Entry(
            form_frame,
            textvariable=self.payment_amount_var,
            font=('Segoe UI', 10)
        )
        payment_amount_entry.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Fecha de pago
        tk.Label(form_frame, text="Fecha:", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=2)
        self.payment_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        payment_date_entry = tk.Entry(
            form_frame,
            textvariable=self.payment_date_var,
            font=('Segoe UI', 10)
        )
        payment_date_entry.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Botón de registrar pago
        register_btn = tk.Button(
            parent,
            text="💰 Registrar Pago",
            font=('Segoe UI', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.register_payment
        )
        register_btn.pack(pady=(0, 15), padx=15)
        
        # Inicialmente ocultar formulario
        self.hide_payment_form()
    
    def hide_payment_form(self):
        """Oculta el formulario de pago"""
        # Por ahora, no ocultamos el formulario
        pass
    
    def load_students_list(self):
        """Carga la lista de estudiantes para el buscador"""
        try:
            students = student_repo.get_all()
            if not students:
                self.show_student_error("No hay estudiantes registrados")
                return
            
            # Filtrar estudiantes activos
            self.all_students = [s for s in students if s.get('enrollment_status') == 'activo']
            self.filtered_students = self.all_students.copy()
            
            # Actualizar tabla
            self.populate_students_table(self.filtered_students)
            
        except Exception as e:
            print(f"Error cargando estudiantes: {e}")
            self.show_student_error("Error al cargar estudiantes")
    
    def filter_students(self):
        """Filtra estudiantes según el texto de búsqueda"""
        search_text = self.student_search_var.get().lower()
        
        if not search_text:
            self.filtered_students = self.all_students.copy()
        else:
            self.filtered_students = [
                s for s in self.all_students
                if search_text in s.get('first_name', '').lower() or
                   search_text in s.get('last_name', '').lower()
            ]
        
        self.populate_students_table(self.filtered_students)
    
    def populate_students_table(self, students):
        """Llena la tabla con datos de estudiantes"""
        # Limpiar tabla
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Agregar estudiantes
        for student in students:
            try:
                # Obtener resumen financiero del estudiante
                summary = self.finance_service.get_student_financial_summary(student['id'])
                metrics = summary['financial_metrics']
                
                # Determinar estado financiero
                status = summary['payment_status']
                status_text = status.replace('_', ' ').title()
                
                # Color según estado
                if status == 'al_dia':
                    status_text = f"✅ {status_text}"
                elif status == 'moroso':
                    status_text = f"⚠️ {status_text}"
                else:
                    status_text = f"⏳ {status_text}"
                
                self.students_tree.insert('', 'end', values=(
                    student['first_name'],
                    student['last_name'],
                    status_text,
                    f"{metrics.outstanding:.2f} FCFA"
                ))
                
            except Exception as e:
                print(f"Error obteniendo datos del estudiante {student['id']}: {e}")
                self.students_tree.insert('', 'end', values=(
                    student['first_name'],
                    student['last_name'],
                    "Error",
                    "N/A"
                ))
    
    def on_student_select(self, event):
        """Maneja la selección de un estudiante"""
        selection = self.students_tree.selection()
        if not selection:
            return
        
        # Obtener el índice del estudiante seleccionado
        item = self.students_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Buscar el estudiante correspondiente
        student_name = values[0]
        student_lastname = values[1]
        
        selected_student = None
        for student in self.filtered_students:
            if (student['first_name'] == student_name and 
                student['last_name'] == student_lastname):
                selected_student = student
                break
        
        if selected_student:
            self.load_student_details(selected_student)
    
    def load_student_details(self, student):
        """Carga los detalles del estudiante seleccionado"""
        try:
            # Obtener resumen financiero completo
            summary = self.finance_service.get_student_financial_summary(student['id'])
            
            # Actualizar información básica
            self.student_name_label.config(
                text=f"{student['first_name']} {student['last_name']}"
            )
            
            tutor_name = student.get('tutor_name', 'No especificado')
            self.student_tutor_label.config(text=f"Tutor: {tutor_name}")
            
            # Estado financiero
            status = summary['payment_status']
            risk_level = summary['risk_level']
            
            status_text = status.replace('_', ' ').title()
            if status == 'al_dia':
                status_color = '#27ae60'
                status_text = f"✅ {status_text}"
            elif status == 'moroso':
                status_color = '#e74c3c'
                status_text = f"⚠️ {status_text}"
            else:
                status_color = '#f39c12'
                status_text = f"⏳ {status_text}"
            
            self.student_status_label.config(
                text=f"{status_text} (Riesgo: {risk_level.title()})",
                fg=status_color
            )
            
            # Actualizar tabla de pagos
            self.populate_payments_table(summary['payment_details'])
            
            # Actualizar formulario de pago
            self.update_payment_form(student['id'], summary['payment_details'])
            
        except Exception as e:
            print(f"Error cargando detalles del estudiante: {e}")
            self.show_student_error("Error al cargar detalles del estudiante")
    
    def populate_payments_table(self, payments):
        """Llena la tabla de pagos del estudiante"""
        # Limpiar tabla
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)
        
        # Agregar pagos
        for payment in payments:
            # Formatear estado
            status = payment['status']
            if status == 'pagado':
                status_text = f"✅ {status.title()}"
            elif status == 'retrasado':
                status_text = f"⚠️ {status.title()}"
            else:
                status_text = f"⏳ {status.title()}"
            
            self.payments_tree.insert('', 'end', values=(
                f"{payment['amount_due']:.2f} FCFA",
                f"{payment['amount_paid']:.2f} FCFA",
                status_text,
                payment.get('due_date', 'N/A')
            ))
    
    def update_payment_form(self, student_id, payments):
        """Actualiza el formulario de pago con los pagos pendientes"""
        # Filtrar pagos pendientes
        pending_payments = [p for p in payments if p['status'] != 'pagado']
        
        if not pending_payments:
            self.payment_combo['values'] = []
            self.payment_var.set("")
            return
        
        # Crear opciones para el combo
        payment_options = []
        for payment in pending_payments:
            remaining = payment['amount_due'] - payment['amount_paid']
            option = f"Pago {payment['id']} - {remaining:.2f} FCFA pendientes"
            payment_options.append(option)
        
        self.payment_combo['values'] = payment_options
        
        # Seleccionar primer pago por defecto
        if payment_options:
            self.payment_var.set(payment_options[0])
        
        # Guardar referencia a los pagos
        self.current_student_id = student_id
        self.current_payments = pending_payments
    
    def register_payment(self):
        """Registra un pago para el estudiante seleccionado"""
        try:
            # Validar que hay estudiante seleccionado
            if not hasattr(self, 'current_student_id'):
                messagebox.showerror("Error", "Por favor seleccione un estudiante")
                return
            
            # Validar formulario
            if not self.payment_var.get():
                messagebox.showerror("Error", "Por favor seleccione un pago")
                return
            
            if not self.payment_amount_var.get():
                messagebox.showerror("Error", "Por favor ingrese el monto")
                return
            
            # Obtener datos del formulario
            selected_payment_text = self.payment_var.get()
            payment_id = int(selected_payment_text.split()[1])
            amount = float(self.payment_amount_var.get())
            
            # Validar monto
            selected_payment = None
            for payment in self.current_payments:
                if payment['id'] == payment_id:
                    selected_payment = payment
                    break
            
            if not selected_payment:
                messagebox.showerror("Error", "Pago no encontrado")
                return
            
            remaining = selected_payment['amount_due'] - selected_payment['amount_paid']
            if amount > remaining:
                messagebox.showerror("Error", f"El monto excede el saldo pendiente de {remaining:.2f} FCFA")
                return
            
            # Registrar pago
            success = self.finance_service.record_payment(payment_id, amount)
            
            if success:
                messagebox.showinfo("Éxito", f"Pago de {amount:.2f} FCFA registrado correctamente")
                
                # Limpiar formulario
                self.payment_amount_var.set("")
                
                # Recargar datos del estudiante
                student = student_repo.get_by_id(self.current_student_id)
                if student:
                    self.load_student_details(student)
                
                # Actualizar lista de estudiantes
                self.load_students_list()
            else:
                messagebox.showerror("Error", "No se pudo registrar el pago")
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto válido")
        except Exception as e:
            print(f"Error registrando pago: {e}")
            messagebox.showerror("Error", "Ocurrió un error al registrar el pago")
    
    def show_student_error(self, message: str):
        """Muestra un mensaje de error en la sección de estudiantes"""
        # Limpiar tabla
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Insertar mensaje de error
        self.students_tree.insert('', 'end', values=(
            message, '', '', ''
        ))
    
    def show_morosidad_section(self):
        """Muestra la sección de morosidad"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y filtros
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="⚠️ Control de Morosidad",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Filtros
        filter_frame = tk.Frame(title_frame, bg='white')
        filter_frame.pack(side='right')
        
        tk.Label(filter_frame, text="Filtro:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.morosidad_filter_var = tk.StringVar(value="Todos")
        morosidad_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.morosidad_filter_var,
            values=["Todos", "Críticos (+60 días)", "Recientes (-30 días)"],
            font=('Segoe UI', 10),
            width=20,
            state='readonly'
        )
        morosidad_combo.pack(side='left')
        morosidad_combo.bind('<<ComboboxSelected>>', lambda e: self.load_morosidad_data())
        
        # Botón de actualizar
        refresh_btn = tk.Button(
            filter_frame,
            text="🔄",
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.load_morosidad_data
        )
        refresh_btn.pack(side='left', padx=(10, 0))
        
        # Tarjetas de métricas
        self.create_morosidad_metric_cards()
        
        # Tabla de morosidad
        self.create_morosidad_table()
        
        # Cargar datos iniciales
        self.load_morosidad_data()
    
    def create_morosidad_metric_cards(self):
        """Crea las tarjetas de métricas para morosidad"""
        cards_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        cards_frame.pack(fill='x', pady=(0, 10))
        
        # Tarjeta: Total Morosos
        self.total_overdue_card = self.create_metric_card(
            cards_frame,
            "⚠️ Total Morosos",
            "0",
            "#e74c3c",
            0
        )
        
        # Tarjeta: Monto Vencido
        self.overdue_amount_card = self.create_metric_card(
            cards_frame,
            "💸 Monto Vencido",
            "0 FCFA",
            "#e74c3c",
            1
        )
        
        # Tarjeta: Críticos (>60 días)
        self.critical_overdue_card = self.create_metric_card(
            cards_frame,
            "🚨 Críticos (>60 días)",
            "0",
            "#c0392b",
            2
        )
        
        # Tarjeta: Promedio Días Vencido
        self.avg_overdue_days_card = self.create_metric_card(
            cards_frame,
            "📅 Prom. Días Vencido",
            "0",
            "#f39c12",
            3
        )
    
    def create_morosidad_table(self):
        """Crea la tabla de morosidad"""
        # Frame de la tabla
        table_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview (tabla)
        self.morosidad_tree = ttk.Treeview(
            table_frame,
            columns=('Estudiante', 'Tutor', 'MontoPendiente', 'DiasVencido', 'FechaVencimiento'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar columnas
        self.morosidad_tree.heading('Estudiante', text='Estudiante')
        self.morosidad_tree.heading('Tutor', text='Tutor')
        self.morosidad_tree.heading('MontoPendiente', text='Monto Pendiente')
        self.morosidad_tree.heading('DiasVencido', text='Días Vencido')
        self.morosidad_tree.heading('FechaVencimiento', text='Fecha Vencimiento')
        
        # Configurar anchos
        self.morosidad_tree.column('Estudiante', width=200, minwidth=150)
        self.morosidad_tree.column('Tutor', width=180, minwidth=150)
        self.morosidad_tree.column('MontoPendiente', width=120, minwidth=100)
        self.morosidad_tree.column('DiasVencido', width=120, minwidth=100)
        self.morosidad_tree.column('FechaVencimiento', width=140, minwidth=120)
        
        # Empaquetar
        self.morosidad_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
    
    def load_morosidad_data(self):
        """Carga los datos de morosidad"""
        try:
            # Obtener pagos vencidos
            overdue_payments = self.finance_service.get_overdue_payments()
            
            # Aplicar filtro
            filter_type = self.morosidad_filter_var.get()
            filtered_payments = self.apply_morosidad_filter(overdue_payments, filter_type)
            
            # Calcular métricas
            metrics = self.calculate_morosidad_metrics(filtered_payments)
            
            # Actualizar tarjetas
            self.update_morosidad_metrics(metrics)
            
            # Actualizar tabla
            self.populate_morosidad_table(filtered_payments)
            
        except Exception as e:
            print(f"Error cargando datos de morosidad: {e}")
            self.show_morosidad_error("Error al cargar los datos. Por favor, intente nuevamente.")
    
    def apply_morosidad_filter(self, payments, filter_type):
        """Aplica el filtro de morosidad"""
        if filter_type == "Todos":
            return payments
        
        today = date.today()
        filtered = []
        
        for payment in payments:
            if not payment.get('due_date'):
                continue
            
            try:
                due_date = datetime.strptime(payment['due_date'], '%Y-%m-%d').date()
                days_overdue = (today - due_date).days
                
                if filter_type == "Críticos (+60 días)" and days_overdue > 60:
                    filtered.append(payment)
                elif filter_type == "Recientes (-30 días)" and days_overdue <= 30:
                    filtered.append(payment)
                    
            except ValueError:
                continue
        
        return filtered
    
    def calculate_morosidad_metrics(self, payments):
        """Calcula métricas de morosidad"""
        total_overdue = len(payments)
        overdue_amount = sum(p['amount_due'] - p['amount_paid'] for p in payments)
        
        critical_count = 0
        total_days_overdue = 0
        today = date.today()
        
        for payment in payments:
            if payment.get('due_date'):
                try:
                    due_date = datetime.strptime(payment['due_date'], '%Y-%m-%d').date()
                    days_overdue = (today - due_date).days
                    total_days_overdue += days_overdue
                    
                    if days_overdue > 60:
                        critical_count += 1
                except ValueError:
                    continue
        
        avg_days = total_days_overdue / total_overdue if total_overdue > 0 else 0
        
        return {
            'total_overdue': total_overdue,
            'overdue_amount': overdue_amount,
            'critical_count': critical_count,
            'avg_days_overdue': avg_days
        }
    
    def update_morosidad_metrics(self, metrics):
        """Actualiza las tarjetas de métricas de morosidad"""
        self.total_overdue_card.config(text=str(metrics['total_overdue']))
        self.overdue_amount_card.config(text=f"{metrics['overdue_amount']:.2f} FCFA")
        self.critical_overdue_card.config(text=str(metrics['critical_count']))
        self.avg_overdue_days_card.config(text=f"{metrics['avg_days_overdue']:.0f}")
    
    def populate_morosidad_table(self, payments):
        """Llena la tabla con datos de morosidad"""
        # Limpiar tabla
        for item in self.morosidad_tree.get_children():
            self.morosidad_tree.delete(item)
        
        # Agregar pagos vencidos
        today = date.today()
        
        for payment in payments:
            try:
                # Obtener información del estudiante
                student = student_repo.get_by_id(payment['student_id'])
                if not student:
                    continue
                
                # Calcular días vencido
                days_overdue = 0
                if payment.get('due_date'):
                    try:
                        due_date = datetime.strptime(payment['due_date'], '%Y-%m-%d').date()
                        days_overdue = (today - due_date).days
                    except ValueError:
                        days_overdue = 0
                
                # Monto pendiente
                outstanding = payment['amount_due'] - payment['amount_paid']
                
                # Formatear días vencido con color
                if days_overdue > 60:
                    days_text = f"🚨 {days_overdue}"
                elif days_overdue > 30:
                    days_text = f"⚠️ {days_overdue}"
                else:
                    days_text = f"📅 {days_overdue}"
                
                self.morosidad_tree.insert('', 'end', values=(
                    f"{student['first_name']} {student['last_name']}",
                    student.get('tutor_name', 'No especificado'),
                    f"{outstanding:.2f} FCFA",
                    days_text,
                    payment.get('due_date', 'N/A')
                ))
                
            except Exception as e:
                print(f"Error procesando pago vencido {payment['id']}: {e}")
                continue
    
    def show_morosidad_error(self, message: str):
        """Muestra un mensaje de error en morosidad"""
        # Limpiar tabla
        for item in self.morosidad_tree.get_children():
            self.morosidad_tree.delete(item)
        
        # Insertar mensaje de error
        self.morosidad_tree.insert('', 'end', values=(
            message, '', '', '', ''
        ))
    
    def show_tutor_section(self):
        """Muestra la sección de pagos por tutor"""
        # Header de la sección
        header_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título y botones
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="👥 Pagos por Tutor",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Botón de actualizar
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 Actualizar",
            font=('Segoe UI', 10),
            bg='#f39c12',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.load_tutor_data
        )
        refresh_btn.pack(side='right')
        
        # Tarjetas de métricas
        self.create_tutor_metric_cards()
        
        # Tabla de tutores
        self.create_tutor_table()
        
        # Cargar datos iniciales
        self.load_tutor_data()
    
    def create_tutor_metric_cards(self):
        """Crea las tarjetas de métricas para tutores"""
        cards_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        cards_frame.pack(fill='x', pady=(0, 10))
        
        # Tarjeta: Total Tutores
        self.total_tutors_card = self.create_metric_card(
            cards_frame,
            "👥 Total Tutores",
            "0",
            "#3498db",
            0
        )
        
        # Tarjeta: Total Estudiantes
        self.tutor_students_card = self.create_metric_card(
            cards_frame,
            "📚 Total Estudiantes",
            "0",
            "#27ae60",
            1
        )
        
        # Tarjeta: Cobro Promedio
        self.avg_collection_card = self.create_metric_card(
            cards_frame,
            "📈 Cobro Promedio",
            "0.0%",
            "#f39c12",
            2
        )
        
        # Tarjeta: Tutores con Problemas
        self.problem_tutors_card = self.create_metric_card(
            cards_frame,
            "⚠️ Tutores con Problemas",
            "0",
            "#e74c3c",
            3
        )
    
    def create_tutor_table(self):
        """Crea la tabla de tutores"""
        # Frame de la tabla
        table_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview (tabla)
        self.tutor_tree = ttk.Treeview(
            table_frame,
            columns=('Tutor', 'Estudiantes', 'TotalDue', 'TotalPaid', 'Pendiente', 'Vencidos', 'TasaCobro'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar columnas
        self.tutor_tree.heading('Tutor', text='Tutor')
        self.tutor_tree.heading('Estudiantes', text='Estudiantes')
        self.tutor_tree.heading('TotalDue', text='Total Debido')
        self.tutor_tree.heading('TotalPaid', text='Total Pagado')
        self.tutor_tree.heading('Pendiente', text='Pendiente')
        self.tutor_tree.heading('Vencidos', text='Vencidos')
        self.tutor_tree.heading('TasaCobro', text='Tasa Cobro')
        
        # Configurar anchos
        self.tutor_tree.column('Tutor', width=200, minwidth=150)
        self.tutor_tree.column('Estudiantes', width=100, minwidth=80)
        self.tutor_tree.column('TotalDue', width=120, minwidth=100)
        self.tutor_tree.column('TotalPaid', width=120, minwidth=100)
        self.tutor_tree.column('Pendiente', width=120, minwidth=100)
        self.tutor_tree.column('Vencidos', width=100, minwidth=80)
        self.tutor_tree.column('TasaCobro', width=100, minwidth=80)
        
        # Empaquetar
        self.tutor_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
    
    def load_tutor_data(self):
        """Carga los datos de tutores"""
        try:
            # Obtener grupos de tutores
            tutor_groups = self.finance_service.get_tutor_payment_groups()
            
            # Calcular métricas generales
            metrics = self.calculate_tutor_metrics(tutor_groups)
            
            # Actualizar tarjetas
            self.update_tutor_metrics(metrics)
            
            # Actualizar tabla
            self.populate_tutor_table(tutor_groups)
            
        except Exception as e:
            print(f"Error cargando datos de tutores: {e}")
            self.show_tutor_error("Error al cargar los datos. Por favor, intente nuevamente.")
    
    def calculate_tutor_metrics(self, tutor_groups):
        """Calcula métricas generales de tutores"""
        total_tutors = len(tutor_groups)
        total_students = sum(group.students_count for group in tutor_groups)
        
        total_due = sum(group.total_due for group in tutor_groups)
        total_paid = sum(group.total_paid for group in tutor_groups)
        
        avg_collection = (total_paid / total_due * 100) if total_due > 0 else 0
        
        problem_tutors = len([
            group for group in tutor_groups 
            if group.overdue_count > 0 or group.outstanding > 0
        ])
        
        return {
            'total_tutors': total_tutors,
            'total_students': total_students,
            'avg_collection': avg_collection,
            'problem_tutors': problem_tutors
        }
    
    def update_tutor_metrics(self, metrics):
        """Actualiza las tarjetas de métricas de tutores"""
        self.total_tutors_card.config(text=str(metrics['total_tutors']))
        self.tutor_students_card.config(text=str(metrics['total_students']))
        self.avg_collection_card.config(text=f"{metrics['avg_collection']:.1f}%")
        self.problem_tutors_card.config(text=str(metrics['problem_tutors']))
    
    def populate_tutor_table(self, tutor_groups):
        """Llena la tabla con datos de tutores"""
        # Limpiar tabla
        for item in self.tutor_tree.get_children():
            self.tutor_tree.delete(item)
        
        # Ordenar por monto pendiente (mayor a menor)
        sorted_groups = sorted(tutor_groups, key=lambda x: x.outstanding, reverse=True)
        
        # Agregar grupos de tutores
        for group in sorted_groups:
            # Calcular tasa de cobro
            collection_rate = (group.total_paid / group.total_due * 100) if group.total_due > 0 else 0
            
            # Formatear estado con indicadores visuales
            if group.overdue_count > 0:
                tutor_name = f"⚠️ {group.tutor_name}"
            elif group.outstanding > 0:
                tutor_name = f"⏳ {group.tutor_name}"
            else:
                tutor_name = f"✅ {group.tutor_name}"
            
            # Formatear tasa de cobro con color
            if collection_rate >= 90:
                rate_text = f"🟢 {collection_rate:.1f}%"
            elif collection_rate >= 70:
                rate_text = f"🟡 {collection_rate:.1f}%"
            else:
                rate_text = f"🔴 {collection_rate:.1f}%"
            
            self.tutor_tree.insert('', 'end', values=(
                tutor_name,
                group.students_count,
                f"{group.total_due:.2f} FCFA",
                f"{group.total_paid:.2f} FCFA",
                f"{group.outstanding:.2f} FCFA",
                group.overdue_count,
                rate_text
            ))
    
    def show_tutor_error(self, message: str):
        """Muestra un mensaje de error en la sección de tutores"""
        # Limpiar tabla
        for item in self.tutor_tree.get_children():
            self.tutor_tree.delete(item)
        
        # Insertar mensaje de error
        self.tutor_tree.insert('', 'end', values=(
            message, '', '', '', '', '', ''
        ))
