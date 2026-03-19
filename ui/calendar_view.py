"""
Calendar View - Gestión de Calendarios de Pagos
Interfaz para administración de calendarios de pagos por tutor
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional

from services.finance_service import FinanceService
from database.repository import student_repo


class CalendarManagerView:
    """Vista principal para gestión de calendarios de pagos"""
    
    def __init__(self, parent: tk.Widget, finance_service: FinanceService):
        self.parent = parent
        self.finance_service = finance_service
        self.calendars_data = []
        self.current_calendar = None
        
        self.setup_ui()
        self.load_calendars()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Frame principal
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de herramientas
        self.setup_toolbar()
        
        # Lista de calendarios
        self.setup_calendar_list()
        
        # Frame de detalles (inicialmente oculto)
        self.details_frame = ttk.Frame(self.main_frame)
        
    def setup_toolbar(self):
        """Configura la barra de herramientas"""
        
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Botones
        ttk.Button(
            toolbar, 
            text="➕ Nuevo Calendario",
            command=self.show_create_calendar_dialog
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar,
            text="🔄 Actualizar",
            command=self.load_calendars
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Buscador
        ttk.Label(toolbar, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_calendars)
        ttk.Entry(
            toolbar,
            textvariable=self.search_var,
            width=20
        ).pack(side=tk.LEFT)
        
    def setup_calendar_list(self):
        """Configura la lista de calendarios"""
        
        # Frame con scroll
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(list_frame, bg='white')
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def load_calendars(self):
        """Carga la lista de calendarios activos"""
        
        try:
            calendars = self.finance_service.payment_calendar_repo.get_active_calendars()
            self.calendars_data = []
            
            for calendar in calendars:
                # Obtener detalles completos
                calendar_details = self.finance_service.payment_calendar_repo.get_with_details(calendar['id'])
                if calendar_details:
                    self.calendars_data.append(calendar_details)
            
            self.render_calendar_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los calendarios: {str(e)}")
    
    def render_calendar_list(self):
        """Renderiza la lista de calendarios en el canvas"""
        
        # Limpiar canvas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.calendars_data:
            ttk.Label(
                self.scrollable_frame,
                text="No hay calendarios activos",
                font=('Arial', 12)
            ).pack(pady=20)
            return
        
        # Renderizar cada calendario
        for i, calendar in enumerate(self.calendars_data):
            self.render_calendar_card(calendar, i)
    
    def render_calendar_card(self, calendar: Dict[str, Any], index: int):
        """Renderiza una tarjeta de calendario"""
        
        # Frame de la tarjeta
        card = ttk.Frame(self.scrollable_frame, relief=tk.RIDGE, borderwidth=1)
        card.pack(fill=tk.X, padx=5, pady=5)
        
        # Calcular progreso
        installments = calendar.get('installments', [])
        paid_count = sum(1 for inst in installments if inst['status'] == 'pagado')
        total_count = len(installments)
        progress = f"{paid_count}/{total_count}" if total_count > 0 else "0/0"
        
        # Obtener último pago
        last_payment = "Sin pagos"
        paid_installments = [inst for inst in installments if inst['status'] == 'pagado']
        if paid_installments:
            last_paid = max(paid_installments, key=lambda x: x.get('paid_date', ''))
            last_payment = last_paid.get('paid_date', 'Sin fecha')
        
        # Frame principal
        main_frame = ttk.Frame(card)
        main_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Columna izquierda - Información
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(
            left_frame,
            text=f"Tutor: {calendar['tutor_name']}",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W)
        
        ttk.Label(
            left_frame,
            text=f"Total: {calendar['final_amount']:,.0f} FCFA"
        ).pack(anchor=tk.W)
        
        ttk.Label(
            left_frame,
            text=f"Estado: {calendar['status'].title()}"
        ).pack(anchor=tk.W)
        
        # Columna derecha - Progreso y acciones
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Label(
            right_frame,
            text=f"Progreso: {progress}"
        ).pack(anchor=tk.E)
        
        ttk.Label(
            right_frame,
            text=f"Hijos: {len(calendar.get('students', []))}"
        ).pack(anchor=tk.E)
        
        ttk.Label(
            right_frame,
            text=f"Último pago: {last_payment}"
        ).pack(anchor=tk.E)
        
        # Botones de acción
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=(5, 0))
        
        ttk.Button(
            button_frame,
            text="📋 Detalles",
            command=lambda c=calendar: self.show_calendar_details(c)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="💰 Pagar",
            command=lambda c=calendar: self.quick_payment(c)
        ).pack(side=tk.LEFT)
    
    def show_create_calendar_dialog(self):
        """Muestra diálogo para crear nuevo calendario"""
        
        dialog = CreateCalendarDialog(self.parent, self.finance_service)
        if dialog.result:
            self.load_calendars()
            messagebox.showinfo("Éxito", "Calendario creado correctamente")
    
    def show_calendar_details(self, calendar: Dict[str, Any]):
        """Muestra vista detallada del calendario"""
        
        # Ocultar lista
        self.canvas.pack_forget()
        
        # Mostrar detalles
        self.details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Limpiar y configurar detalles
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        self.setup_details_view(calendar)
    
    def setup_details_view(self, calendar: Dict[str, Any]):
        """Configura vista de detalles del calendario"""
        
        self.current_calendar = calendar
        
        # Header
        header = ttk.Frame(self.details_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header,
            text=f"Calendario: {calendar['tutor_name']} - Año {calendar['academic_year']}",
            font=('Arial', 14, 'bold')
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header,
            text="← Volver",
            command=self.hide_details
        ).pack(side=tk.RIGHT)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.details_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de cuotas
        self.setup_installments_tab(notebook, calendar)
        
        # Pestaña de estudiantes
        self.setup_students_tab(notebook, calendar)
    
    def setup_installments_tab(self, notebook: ttk.Notebook, calendar: Dict[str, Any]):
        """Configura pestaña de cuotas"""
        
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text="💰 Cuotas")
        
        # Lista de cuotas
        installments_frame = ttk.Frame(tab_frame)
        installments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = ttk.Frame(installments_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Cuota", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(header, text="Monto", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(header, text="Vence", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(header, text="Estado", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(header, text="Acciones", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Lista de cuotas
        installments = calendar.get('installments', [])
        for installment in installments:
            self.render_installment_row(installments_frame, installment)
        
        # Botón de registro de pago
        ttk.Button(
            tab_frame,
            text="💳 Registrar Pago",
            command=lambda: self.register_payment(calendar)
        ).pack(pady=10)
    
    def render_installment_row(self, parent: ttk.Frame, installment: Dict[str, Any]):
        """Renderiza una fila de cuota"""
        
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)
        
        # Datos
        ttk.Label(row_frame, text=f"Cuota {installment['installment_number']}").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(row_frame, text=f"{installment['amount']:,.0f} FCFA").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(row_frame, text=installment['due_date']).pack(side=tk.LEFT, padx=(0, 20))
        
        # Estado con color
        status_text = installment['status'].title()
        if installment['status'] == 'pagado':
            status_text = f"✅ {status_text}"
        elif installment['status'] == 'vencido':
            status_text = f"⚠️ {status_text}"
        else:
            status_text = f"⏳ {status_text}"
        
        ttk.Label(row_frame, text=status_text).pack(side=tk.LEFT, padx=(0, 20))
        
        # Acciones
        if installment['status'] != 'pagado':
            ttk.Button(
                row_frame,
                text="Pagar",
                command=lambda i=installment: self.pay_installment(i)
            ).pack(side=tk.LEFT)
    
    def setup_students_tab(self, notebook: ttk.Notebook, calendar: Dict[str, Any]):
        """Configura pestaña de estudiantes"""
        
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text="👥 Estudiantes")
        
        # Lista de estudiantes
        students_frame = ttk.Frame(tab_frame)
        students_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = ttk.Frame(students_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Estudiante", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(header, text="Matrícula", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 20))
        
        # Lista de estudiantes
        students = calendar.get('students', [])
        for student in students:
            row_frame = ttk.Frame(students_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            name = f"{student['first_name']} {student['last_name']}"
            enrollment = f"{student['enrollment_price']:,.0f} FCFA"
            
            ttk.Label(row_frame, text=name).pack(side=tk.LEFT, padx=(0, 20))
            ttk.Label(row_frame, text=enrollment).pack(side=tk.LEFT, padx=(0, 20))
        
        # Resumen financiero
        summary_frame = ttk.LabelFrame(students_frame, text="Resumen Financiero")
        summary_frame.pack(fill=tk.X, pady=(20, 10))
        
        total_base = sum(s['enrollment_price'] for s in students)
        
        ttk.Label(summary_frame, text=f"Total Base: {total_base:,.0f} FCFA").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(summary_frame, text=f"Descuento: {calendar['discount_amount']:,.0f} FCFA").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(summary_frame, text=f"Total Final: {calendar['final_amount']:,.0f} FCFA", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=2)
        
        # Botón para añadir estudiante
        ttk.Button(
            tab_frame,
            text="➕ Añadir Estudiante",
            command=lambda: self.add_student_to_calendar(calendar)
        ).pack(pady=10)
    
    def hide_details(self):
        """Oculta vista de detalles y muestra lista"""
        
        self.details_frame.pack_forget()
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.current_calendar = None
    
    def filter_calendars(self, *args):
        """Filtra calendarios basado en búsqueda"""
        
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.render_calendar_list()
            return
        
        filtered = [
            cal for cal in self.calendars_data
            if search_term in cal['tutor_name'].lower()
        ]
        
        # Temporalmente reemplazar datos para renderizado
        original_data = self.calendars_data
        self.calendars_data = filtered
        self.render_calendar_list()
        self.calendars_data = original_data
    
    def register_payment(self, calendar: Dict[str, Any]):
        """Registra pago para una cuota específica"""
        
        # Obtener cuotas pendientes
        pending_installments = [
            inst for inst in calendar.get('installments', [])
            if inst['status'] != 'pagado'
        ]
        
        if not pending_installments:
            messagebox.showinfo("Información", "No hay cuotas pendientes")
            return
        
        # Diálogo para seleccionar cuota
        installment_names = [
            f"Cuota {inst['installment_number']} - {inst['amount']:,.0f} FCFA - Vence: {inst['due_date']}"
            for inst in pending_installments
        ]
        
        selected_index = simpledialog.askinteger(
            "Seleccionar Cuota",
            "Seleccione el número de cuota a pagar:\n\n" + "\n".join(
                f"{i+1}. {name}" for i, name in enumerate(installment_names)
            ),
            minvalue=1,
            maxvalue=len(pending_installments)
        )
        
        if selected_index:
            installment = pending_installments[selected_index - 1]
            self.pay_installment(installment)
    
    def pay_installment(self, installment: Dict[str, Any]):
        """Procesa pago de una cuota específica"""
        
        dialog = PaymentDialog(self.parent, installment)
        if dialog.result:
            self.load_calendars()
            if self.current_calendar:
                # Recargar detalles si estamos en vista de detalles
                updated_calendar = self.finance_service.payment_calendar_repo.get_with_details(self.current_calendar['id'])
                self.setup_details_view(updated_calendar)
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
    
    def quick_payment(self, calendar: Dict[str, Any]):
        """Pago rápido desde la lista principal"""
        
        pending_installments = [
            inst for inst in calendar.get('installments', [])
            if inst['status'] != 'pagado'
        ]
        
        if not pending_installments:
            messagebox.showinfo("Información", "No hay cuotas pendientes")
            return
        
        # Pagar la primera cuota pendiente
        self.pay_installment(pending_installments[0])
    
    def add_student_to_calendar(self, calendar: Dict[str, Any]):
        """Añade estudiante al calendario"""
        
        dialog = AddStudentDialog(self.parent, self.finance_service, calendar)
        if dialog.result:
            self.load_calendars()
            if self.current_calendar:
                updated_calendar = self.finance_service.payment_calendar_repo.get_with_details(self.current_calendar['id'])
                self.setup_details_view(updated_calendar)
            messagebox.showinfo("Éxito", "Estudiante añadido correctamente")


class CreateCalendarDialog:
    """Diálogo para crear nuevo calendario"""
    
    def __init__(self, parent: tk.Widget, finance_service: FinanceService):
        self.parent = parent
        self.finance_service = finance_service
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Calendario de Pagos")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_dialog()
        
        self.dialog.wait_window()
    
    def setup_ui(self):
        """Configura interfaz del diálogo"""
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Datos del tutor
        tutor_frame = ttk.LabelFrame(main_frame, text="Datos del Tutor")
        tutor_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(tutor_frame, text="Nombre del Tutor:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.tutor_name_var = tk.StringVar()
        ttk.Entry(tutor_frame, textvariable=self.tutor_name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(tutor_frame, text="Teléfono:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.tutor_phone_var = tk.StringVar()
        ttk.Entry(tutor_frame, textvariable=self.tutor_phone_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(tutor_frame, text="Año Académico:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.academic_year_var = tk.IntVar(value=date.today().year)
        ttk.Entry(tutor_frame, textvariable=self.academic_year_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(tutor_frame, text="Descuento (FCFA):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.discount_var = tk.DoubleVar(value=0)
        ttk.Entry(tutor_frame, textvariable=self.discount_var, width=30).grid(row=3, column=1, padx=10, pady=5)
        
        # Estudiantes
        students_frame = ttk.LabelFrame(main_frame, text="Estudiantes a Incluir")
        students_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Lista de estudiantes activos
        self.setup_students_list(students_frame)
        
        # Configuración de cuotas
        installments_frame = ttk.LabelFrame(main_frame, text="Configuración de Cuotas")
        installments_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(installments_frame, text="Número de cuotas:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.installments_count_var = tk.IntVar(value=10)
        ttk.Entry(installments_frame, textvariable=self.installments_count_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(installments_frame, text="Fecha de inicio:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.start_date_var = tk.StringVar(value=date.today().replace(day=1).strftime('%Y-%m-%d'))
        ttk.Entry(installments_frame, textvariable=self.start_date_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        # Resumen
        self.summary_frame = ttk.LabelFrame(main_frame, text="Resumen")
        self.summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.total_base_label = ttk.Label(self.summary_frame, text="Total Base: 0 FCFA")
        self.total_base_label.pack(anchor=tk.W, padx=10, pady=2)
        
        self.discount_label = ttk.Label(self.summary_frame, text="Descuento: 0 FCFA")
        self.discount_label.pack(anchor=tk.W, padx=10, pady=2)
        
        self.total_final_label = ttk.Label(self.summary_frame, text="Total Final: 0 FCFA", font=('Arial', 10, 'bold'))
        self.total_final_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Crear Calendario", command=self.create_calendar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Binds para actualización automática
        self.tutor_name_var.trace('w', self.update_summary)
        self.discount_var.trace('w', self.update_summary)
        
        self.update_summary()
    
    def setup_students_list(self, parent: ttk.Frame):
        """Configura lista de estudiantes seleccionables"""
        
        # Frame con scroll
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(list_frame, height=150)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar estudiantes
        try:
            all_students = student_repo.get_all()
            students = [s for s in all_students if s.get('enrollment_status') == 'activo']
            self.student_vars = {}
            
            for student in students:
                # Obtener precio de matrícula
                try:
                    price = self.finance_service._get_student_enrollment_price(
                        student['id'], self.academic_year_var.get()
                    )
                except:
                    price = 0
                
                # Checkbox
                var = tk.BooleanVar()
                self.student_vars[student['id']] = {
                    'var': var,
                    'student': student,
                    'price': price
                }
                
                frame = ttk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, pady=2)
                
                ttk.Checkbutton(
                    frame,
                    text=f"{student['first_name']} {student['last_name']} - {price:,.0f} FCFA",
                    variable=var,
                    command=self.update_summary
                ).pack(side=tk.LEFT)
                
        except Exception as e:
            ttk.Label(list_frame, text=f"Error cargando estudiantes: {str(e)}").pack()
    
    def update_summary(self, *args):
        """Actualiza resumen de montos"""
        
        total_base = 0
        selected_count = 0
        
        for student_id, data in self.student_vars.items():
            if data['var'].get():
                total_base += data['price']
                selected_count += 1
        
        discount = self.discount_var.get()
        total_final = max(0, total_base - discount)
        
        self.total_base_label.config(text=f"Total Base: {total_base:,.0f} FCFA")
        self.discount_label.config(text=f"Descuento: {discount:,.0f} FCFA")
        self.total_final_label.config(text=f"Total Final: {total_final:,.0f} FCFA")
    
    def create_calendar(self):
        """Crea el calendario"""
        
        try:
            # Validaciones
            tutor_name = self.tutor_name_var.get().strip()
            if not tutor_name:
                messagebox.showerror("Error", "El nombre del tutor es obligatorio")
                return
            
            # Obtener estudiantes seleccionados
            selected_students = [
                student_id for student_id, data in self.student_vars.items()
                if data['var'].get()
            ]
            
            if not selected_students:
                messagebox.showerror("Error", "Debe seleccionar al menos un estudiante")
                return
            
            # Crear calendario
            calendar_id = self.finance_service.create_payment_calendar(
                tutor_name=tutor_name,
                tutor_phone=self.tutor_phone_var.get(),
                student_ids=selected_students,
                discount=self.discount_var.get(),
                academic_year=self.academic_year_var.get()
            )
            
            # Generar cuotas
            installments_count = self.installments_count_var.get()
            start_date = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d').date()
            calendar = self.finance_service.payment_calendar_repo.get_by_id(calendar_id)
            
            installments_list = []
            for i in range(installments_count):
                due_date = (start_date.replace(day=1) + timedelta(days=32*i)).replace(day=1)
                installments_list.append({
                    'amount': calendar['final_amount'] / installments_count,
                    'due_date': due_date.strftime('%Y-%m-%d')
                })
            
            self.finance_service.add_installments(calendar_id, installments_list)
            
            self.result = calendar_id
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el calendario: {str(e)}")
    
    def center_dialog(self):
        """Centra el diálogo en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")


class PaymentDialog:
    """Diálogo para registrar pago"""
    
    def __init__(self, parent: tk.Widget, installment: Dict[str, Any]):
        self.parent = parent
        self.installment = installment
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Registrar Pago - Cuota {installment['installment_number']}")
        self.dialog.geometry("400x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_dialog()
        
        self.dialog.wait_window()
    
    def setup_ui(self):
        """Configura interfaz del diálogo"""
        
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Información de la cuota
        info_frame = ttk.LabelFrame(main_frame, text="Información de Cuota")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Cuota: {self.installment['installment_number']}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(info_frame, text=f"Monto: {self.installment['amount']:,.0f} FCFA").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(info_frame, text=f"Vence: {self.installment['due_date']}").pack(anchor=tk.W, padx=10, pady=2)
        
        # Formulario de pago
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Pago")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Monto pagado:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.amount_var = tk.DoubleVar(value=self.installment['amount'])
        ttk.Entry(form_frame, textvariable=self.amount_var, width=20).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Fecha de pago:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        ttk.Entry(form_frame, textvariable=self.date_var, width=20).grid(row=1, column=1, padx=10, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Confirmar Pago", command=self.confirm_payment).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def confirm_payment(self):
        """Confirma el pago"""
        
        try:
            amount = self.amount_var.get()
            paid_date = self.date_var.get()
            
            if amount <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return
            
            if amount > self.installment['amount']:
                messagebox.showerror("Error", "El monto pagado no puede exceder el monto de la cuota")
                return
            
            # Validar fecha
            datetime.strptime(paid_date, '%Y-%m-%d')
            
            # Registrar pago
            from services.finance_service import finance_service
            finance_service.pay_installment(
                installment_id=self.installment['id'],
                amount=amount,
                paid_date=paid_date
            )
            
            self.result = True
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha inválida: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el pago: {str(e)}")
    
    def center_dialog(self):
        """Centra el diálogo en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")


class AddStudentDialog:
    """Diálogo para añadir estudiante a calendario"""
    
    def __init__(self, parent: tk.Widget, finance_service: FinanceService, calendar: Dict[str, Any]):
        self.parent = parent
        self.finance_service = finance_service
        self.calendar = calendar
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Añadir Estudiante al Calendario")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_dialog()
        
        self.dialog.wait_window()
    
    def setup_ui(self):
        """Configura interfaz del diálogo"""
        
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Información del calendario
        info_frame = ttk.LabelFrame(main_frame, text="Calendario")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Tutor: {self.calendar['tutor_name']}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(info_frame, text=f"Año: {self.calendar['academic_year']}").pack(anchor=tk.W, padx=10, pady=2)
        
        # Lista de estudiantes disponibles
        students_frame = ttk.LabelFrame(main_frame, text="Estudiantes Disponibles")
        students_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame con scroll
        list_frame = ttk.Frame(students_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar estudiantes disponibles
        try:
            # Obtener estudiantes ya en el calendario
            existing_student_ids = {
                s['student_id'] for s in self.calendar.get('students', [])
            }
            
            # Obtener todos los estudiantes activos
            all_students = student_repo.get_all()
            available_students = [
                s for s in all_students 
                if s.get('enrollment_status') == 'activo' and s['id'] not in existing_student_ids
            ]
            
            self.student_vars = {}
            
            for student in available_students:
                # Obtener precio de matrícula
                try:
                    price = self.finance_service._get_student_enrollment_price(
                        student['id'], self.calendar['academic_year']
                    )
                except:
                    price = 0
                
                # Radio button (solo uno a la vez)
                var = tk.IntVar()
                self.student_vars[student['id']] = {
                    'var': var,
                    'student': student,
                    'price': price
                }
                
                frame = ttk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, pady=2)
                
                ttk.Radiobutton(
                    frame,
                    text=f"{student['first_name']} {student['last_name']} - {price:,.0f} FCFA",
                    variable=var,
                    value=student['id']
                ).pack(side=tk.LEFT)
                
        except Exception as e:
            ttk.Label(list_frame, text=f"Error cargando estudiantes: {str(e)}").pack()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Añadir Estudiante", command=self.add_student).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def add_student(self):
        """Añade el estudiante seleccionado"""
        
        try:
            # Obtener estudiante seleccionado
            selected_student_id = None
            for student_id, data in self.student_vars.items():
                if data['var'].get():
                    selected_student_id = student_id
                    break
            
            if not selected_student_id:
                messagebox.showerror("Error", "Debe seleccionar un estudiante")
                return
            
            # Añadir estudiante al calendario
            success = self.finance_service.assign_student_to_calendar(
                student_id=selected_student_id,
                calendar_id=self.calendar['id']
            )
            
            if success:
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "No se pudo añadir el estudiante")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir el estudiante: {str(e)}")
    
    def center_dialog(self):
        """Centra el diálogo en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
