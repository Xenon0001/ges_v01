"""
Dashboard Window - Interfaz principal de GES
Dashboard profesional con métricas clave
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any
from datetime import datetime

from services.student_service import StudentService
from services.academic_service import AcademicService
from services.finance_service import FinanceService


class DashboardWindow:
    """Ventana principal del dashboard"""
    
    def __init__(self, parent: tk.Tk, user_data: Dict[str, Any], 
                 config: Dict[str, Any], on_logout: Callable, 
                 api_client: Optional[Any] = None):  # ← Nuevo parámetro
        self.parent = parent
        self.user_data = user_data
        self.config = config
        self.on_logout = on_logout
        self.user_role = self._get_role_name(user_data.get('role_id', 0))
        
        # Servicios
        # Si tenemos API client, usarlo en lugar de services locales
        if api_client:
            self.student_service = api_client
            self.academic_service = api_client
            self.finance_service = api_client
        else:
            # Modo normal - usar services locales
            self.student_service = StudentService()
            self.academic_service = AcademicService()
            self.finance_service = FinanceService()
        
        # Configurar ventana
        self.setup_window()
        
        # Inicializar metric_cards antes de crear widgets
        self.metric_cards = {}
        
        # Crear UI
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_dashboard_data()
    
    def _get_role_name(self, role_id: int) -> str:
        """Obtiene nombre del rol desde ID"""
        role_names = {
            1: "Directiva",
            2: "Secretaria", 
            3: "Usuario"
        }
        return role_names.get(role_id, "Usuario")
    
    def _check_permission(self, required_role: str) -> bool:
        """Verifica si el usuario tiene permiso para una sección"""
        role_hierarchy = {
            "Directiva": 3,
            "Secretaria": 2,
            "Usuario": 1
        }
        return role_hierarchy.get(self.user_role, 0) >= role_hierarchy.get(required_role, 0)
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.parent.title(f"GES Dashboard - {self.config.get('school_name', 'GES')}")
        self.parent.geometry("1200x700")
        self.parent.resizable(True, True)
        
        # Configurar estilos
        self.setup_styles()
        
        # Maximizar ventana
        self.parent.state('zoomed')
    
    def setup_styles(self):
        """Configura estilos profesionales"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para tarjetas
        style.configure('Card.TFrame',
                     background='white',
                     relief='flat',
                     borderwidth=1)
        
        # Estilo para botones de navegación
        style.configure('Nav.TButton',
                     background='#34495e',
                     foreground='white',
                     borderwidth=0,
                     font=('Segoe UI', 10))
        
        # Estilo para botones de acción
        style.configure('Action.TButton',
                     background='#3498db',
                     foreground='white',
                     borderwidth=0,
                     font=('Segoe UI', 9))
    
    def create_widgets(self):
        """Crea todos los widgets"""
        # Crear layout principal
        self.create_main_layout()
        
        # Crear header
        self.create_header()
        
        # Crear sidebar
        self.create_sidebar()
        
        # Crear contenido principal
        self.create_main_content()
    
    def create_main_layout(self):
        """Crea el layout principal"""
        # Container principal
        self.main_container = tk.Frame(self.parent, bg='#ecf0f1')
        self.main_container.pack(fill='both', expand=True)
        
        # Header
        self.header_frame = tk.Frame(self.main_container, bg='#2c3e50', height=60)
        self.header_frame.pack(fill='x', side='top')
        self.header_frame.pack_propagate(False)
        
        # Contenedor para sidebar y contenido
        self.content_container = tk.Frame(self.main_container, bg='#ecf0f1')
        self.content_container.pack(fill='both', expand=True)
        
        # Sidebar
        self.sidebar_frame = tk.Frame(self.content_container, bg='#34495e', width=250)
        self.sidebar_frame.pack(fill='y', side='left')
        self.sidebar_frame.pack_propagate(False)
        
        # Área de contenido
        self.content_frame = tk.Frame(self.content_container, bg='#ecf0f1')
        self.content_frame.pack(fill='both', expand=True, side='right')
    
    def create_header(self):
        """Crea el header superior"""
        # Logo y título
        left_frame = tk.Frame(self.header_frame, bg='#2c3e50')
        left_frame.pack(side='left', fill='y', padx=20, pady=10)
        
        title_label = tk.Label(
            left_frame,
            text="GES",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', padx=(0, 10))
        
        subtitle_label = tk.Label(
            left_frame,
            text="Sistema de Gestión Escolar",
            font=('Segoe UI', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack(side='left')
        
        # Info de usuario y logout
        right_frame = tk.Frame(self.header_frame, bg='#2c3e50')
        right_frame.pack(side='right', fill='y', padx=20, pady=10)
        
        # Usuario
        user_info = f"{self.user_data.get('username', 'Usuario')} ({self.user_role})"
        user_label = tk.Label(
            right_frame,
            text=user_info,
            font=('Segoe UI', 10),
            fg='white',
            bg='#2c3e50'
        )
        user_label.pack(side='left', padx=(0, 15))
        
        # Botón logout
        logout_btn = tk.Button(
            right_frame,
            text="Cerrar Sesión",
            font=('Segoe UI', 9),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.on_logout
        )
        logout_btn.pack(side='left')
    
    def create_sidebar(self):
        """Crea el sidebar de navegación"""
        # Título del sidebar
        sidebar_title = tk.Label(
            self.sidebar_frame,
            text="Navegación",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg='#34495e'
        )
        sidebar_title.pack(pady=20)
        
        # Navegación principal según rol
        nav_items = self._get_nav_items_for_role()
        
        for text, command, active in nav_items:
            self.create_nav_button(text, command, active)
        
        # Separador
        separator = tk.Frame(self.sidebar_frame, height=2, bg='#2c3e50')
        separator.pack(fill='x', pady=20)
    
    def _get_nav_items_for_role(self) -> list:
        """Obtiene items de navegación según el rol"""
        base_items = [
            ("📊 Dashboard", self.show_dashboard, True),
        ]
        
        if self._check_permission("Secretaria"):
            base_items.extend([
                ("👥 Estudiantes", self.show_students, False),
                ("📚 Académico", self.show_academic, False),
                ("💰 Finanzas", self.show_finances, False),
                ("📈 Reportes", self.show_reports, False),
            ])
        
        if self._check_permission("Directiva"):
            base_items.append(("⚙️ Configuración", self.show_settings, False))
        
        return base_items
        
        # Info del sistema
        info_frame = tk.Frame(self.sidebar_frame, bg='#34495e')
        info_frame.pack(fill='x', padx=20)
        
        year_label = tk.Label(
            info_frame,
            text=f"Año: {self.config.get('academic_year', 2024)}",
            font=('Segoe UI', 9),
            fg='#bdc3c7',
            bg='#34495e'
        )
        year_label.pack(anchor='w')
        
        mode_label = tk.Label(
            info_frame,
            text=f"Modo: {self.config.get('mode', 'normal').title()}",
            font=('Segoe UI', 9),
            fg='#bdc3c7',
            bg='#34495e'
        )
        mode_label.pack(anchor='w', pady=(5, 0))
    
    def create_nav_button(self, text: str, command: Callable, active: bool = False):
        """Crea un botón de navegación"""
        btn = tk.Button(
            self.sidebar_frame,
            text=text,
            font=('Segoe UI', 10),
            bg='#2c3e50' if active else '#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=command,
            anchor='w',
            padx=20,
            pady=10
        )
        btn.pack(fill='x', padx=10, pady=2)
        
        # Efecto hover
        btn.bind('<Enter>', lambda e: btn.configure(bg='#2c3e50'))
        btn.bind('<Leave>', lambda e: btn.configure(bg='#34495e' if not active else '#2c3e50'))
        
        return btn
    
    def create_main_content(self):
        """Crea el contenido principal"""
        # Scrollable frame
        canvas = tk.Canvas(self.content_frame, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Contenido inicial (dashboard)
        self.create_dashboard_content()
    
    def create_dashboard_content(self):
        """Crea el contenido del dashboard"""
        # Limpiar contenido anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Título
        title_label = tk.Label(
            self.scrollable_frame,
            text="Dashboard Principal",
            font=('Segoe UI', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        title_label.pack(pady=20, anchor='w', padx=30)
        
        # Contenedor de tarjetas
        cards_container = tk.Frame(self.scrollable_frame, bg='#ecf0f1')
        cards_container.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Crear tarjetas de métricas
        self.create_metric_cards(cards_container)
        
        # Crear sección de alertas
        self.create_alerts_section(cards_container)
    
    def create_metric_cards(self, parent):
        """Crea las tarjetas de métricas principales"""
        cards_frame = tk.Frame(parent, bg='#ecf0f1')
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Tarjeta 1: Total Estudiantes
        self.create_metric_card(
            cards_frame,
            "👥 Total Estudiantes",
            "0",
            "#3498db",
            0
        )
        
        # Tarjeta 2: Pagos del Mes
        self.create_metric_card(
            cards_frame,
            "💰 Pagos del Mes",
            "€0",
            "#27ae60",
            1
        )
        
        # Tarjeta 3: Morosidad
        self.create_metric_card(
            cards_frame,
            "⚠️ Morosidad",
            "€0",
            "#e74c3c",
            2
        )
        
        # Tarjeta 4: Alertas Activas
        self.create_metric_card(
            cards_frame,
            "🔔 Alertas Activas",
            "0",
            "#f39c12",
            3
        )
    
    def create_metric_card(self, parent, title: str, value: str, color: str, column: int):
        """Crea una tarjeta de métrica individual"""
        card = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        
        # Contenido de la tarjeta
        content_frame = tk.Frame(card, bg='white')
        content_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Título
        title_label = tk.Label(
            content_frame,
            text=title,
            font=('Segoe UI', 12),
            fg='#7f8c8d',
            bg='white'
        )
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Valor
        value_label = tk.Label(
            content_frame,
            text=value,
            font=('Segoe UI', 24, 'bold'),
            fg=color,
            bg='white'
        )
        value_label.pack(anchor='w')
        
        # Guardar referencia para actualizar
        if not hasattr(self, 'metric_cards'):
            self.metric_cards = {}
        self.metric_cards[title] = value_label
    
    def create_alerts_section(self, parent):
        """Crea la sección de alertas"""
        alerts_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        alerts_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header de alertas
        header_frame = tk.Frame(alerts_frame, bg='white')
        header_frame.pack(fill='x', padx=20, pady=20)
        
        alerts_title = tk.Label(
            header_frame,
            text="🔔 Alertas Recientes",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        alerts_title.pack(side='left')
        
        # Contenido de alertas
        self.alerts_content = tk.Frame(alerts_frame, bg='white')
        self.alerts_content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Mensaje inicial
        no_alerts_label = tk.Label(
            self.alerts_content,
            text="No hay alertas activas",
            font=('Segoe UI', 11),
            fg='#95a5a6',
            bg='white'
        )
        no_alerts_label.pack(pady=40)
    
    def load_dashboard_data(self):
        """Carga los datos del dashboard"""
        academic_data = {}
        financial_data = {}
        
        # Cargar datos académicos
        try:
            academic_data = self.academic_service.get_academic_dashboard_data(
                self.config.get('academic_year', 2024)
            )
        except Exception as e:
            print(f"⚠️ Error cargando datos académicos: {e}")
            academic_data = {'critical_alerts': []}
        
        # Cargar datos financieros
        try:
            financial_data = self.finance_service.get_financial_dashboard_data()
        except Exception as e:
            print(f"⚠️ Error cargando datos financieros: {e}")
            financial_data = {'critical_alerts': []}
        
        # Actualizar tarjetas
        try:
            self.update_metric_cards(academic_data, financial_data)
        except Exception as e:
            print(f"⚠️ Error actualizando tarjetas: {e}")
        
        # Actualizar alertas
        try:
            self.update_alerts(financial_data.get('critical_alerts', []))
        except Exception as e:
            print(f"⚠️ Error actualizando alertas: {e}")
    
    def update_metric_cards(self, academic_data: Dict, financial_data: Dict):
        if not hasattr(self, 'metric_cards') or not self.metric_cards:
            return
        if 'summary' in academic_data and "👥 Total Estudiantes" in self.metric_cards:
            total_students = academic_data['summary'].get('total_active_students', 0)
            self.metric_cards["👥 Total Estudiantes"].config(text=str(total_students))
        if 'summary' in financial_data and hasattr(financial_data['summary'], 'total_paid') and "💰 Pagos del Mes" in self.metric_cards:
            self.metric_cards["💰 Pagos del Mes"].config(text=f"€{financial_data['summary'].total_paid:.2f}")
        if 'summary' in financial_data and hasattr(financial_data['summary'], 'total_outstanding') and "⚠️ Morosidad" in self.metric_cards:
            self.metric_cards["⚠️ Morosidad"].config(text=f"€{financial_data['summary'].total_outstanding:.2f}")
        if "🔔 Alertas Activas" in self.metric_cards:
            total_alerts = len(financial_data.get('critical_alerts', [])) + len(academic_data.get('critical_alerts', []))
            self.metric_cards["🔔 Alertas Activas"].config(text=str(total_alerts))
    
    def update_alerts(self, alerts: list):
        """Actualiza la sección de alertas"""
        # Limpiar alertas anteriores
        for widget in self.alerts_content.winfo_children():
            widget.destroy()
        
        if not alerts:
            no_alerts_label = tk.Label(
                self.alerts_content,
                text="No hay alertas críticas",
                font=('Segoe UI', 11),
                fg='#95a5a6',
                bg='white'
            )
            no_alerts_label.pack(pady=40)
        else:
            for alert in alerts[:5]:  # Mostrar máximo 5 alertas
                alert_frame = tk.Frame(self.alerts_content, bg='white')
                alert_frame.pack(fill='x', pady=5)
                
                alert_label = tk.Label(
                    alert_frame,
                    text=f"• {alert.get('message', 'Alerta sin mensaje')}",
                    font=('Segoe UI', 10),
                    fg='#e74c3c',
                    bg='white',
                    anchor='w'
                )
                alert_label.pack(fill='x')
    
    # Métodos de navegación
    def show_dashboard(self):
        """Muestra el dashboard"""
        self.create_dashboard_content()
        self.load_dashboard_data()
    
    def show_students(self):
        """Muestra la vista de estudiantes"""
        if not self._check_permission("Secretaria"):
            messagebox.showwarning("Acceso Denegado", "No tienes permisos para gestionar estudiantes.")
            return
        
        # Limpiar contenido actual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Importar y cargar vista
        from ui.students_view import StudentsView
        StudentsView(self.scrollable_frame, self.config, self.student_service)
    
    def show_academic(self):
        """Muestra la vista académica"""
        if not self._check_permission("Usuario"):
            messagebox.showwarning("Acceso Denegado", "No tienes permisos para acceder a la gestión académica.")
            return
        
        # Limpiar contenido actual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Importar y cargar vista
        from ui.academic_view import AcademicView
        AcademicView(self.scrollable_frame, self.config, self.academic_service)
    
    def show_finances(self):
        """Muestra la vista financiera"""
        if not self._check_permission("Secretaria"):
            messagebox.showwarning("Acceso Denegado", "No tienes permisos para acceder a las finanzas.")
            return
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        from ui.finance_view import FinanceView
        FinanceView(self.scrollable_frame, self.config, self.finance_service)
    
    def show_reports(self):
        """Muestra la vista de reportes"""
        if not self._check_permission("Secretaria"):
            messagebox.showwarning("Acceso Denegado", "No tienes permisos para acceder a los reportes.")
            return
        messagebox.showinfo("En Desarrollo", "Módulo de Reportes en desarrollo")
    
    def show_settings(self):
        """Muestra la configuración"""
        if not self._check_permission("Directiva"):
            messagebox.showwarning("Acceso Denegado", "No tienes permisos para acceder a la configuración.")
            return
        messagebox.showinfo("En Desarrollo", "Módulo de Configuración en desarrollo")
