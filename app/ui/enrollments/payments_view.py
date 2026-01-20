"""
Payments view for GES application
Handles payment management for enrollments
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional
from datetime import datetime, date
from app.services.payment_service import PaymentService
from app.services.enrollment_service import EnrollmentService
from database.models.enrollment import EnrollmentModel, PaymentModel


class PaymentsView(ctk.CTkFrame):
    """Payments management view for an enrollment"""
    
    def __init__(self, parent, enrollment: EnrollmentModel, enrollment_service: EnrollmentService, previous_view=None):
        super().__init__(parent)
        # NO usar pack aquí
        # self.pack(fill="both", expand=True)
        
        self.enrollment = enrollment
        self.enrollment_service = enrollment_service
        self.payment_service = PaymentService()
        self.current_payments = []
        self.selected_payment = None
        self.previous_view = previous_view  # Referencia a la vista anterior
        
        # Configurar grid
        self.grid_rowconfigure(4, weight=1)  # La fila del list_frame
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.load_payments()
    
    def create_widgets(self):
        """Create payments view widgets"""
        # Header with enrollment info and back button
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="← Volver a Matrículas",
            command=self.go_back,
            width=150
        )
        back_button.pack(side="left", padx=10, pady=10)
        
        # Enrollment info
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        student_name = "Estudiante no encontrado"
        if self.enrollment.student and self.enrollment.student.person:
            student_name = f"{self.enrollment.student.person.name} {self.enrollment.student.person.last_name}"
        
        title_label = ctk.CTkLabel(
            info_frame,
            text=f"Pagos - {student_name}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack()
        
        enrollment_text = f"Matrícula: {self.enrollment.enrollment_number}"
        if self.enrollment.grade:
            enrollment_text += f" | {self.enrollment.grade.name}"
        if self.enrollment.academic_year:
            enrollment_text += f" | {self.enrollment.academic_year.name}"
        
        enrollment_label = ctk.CTkLabel(
            info_frame,
            text=enrollment_text,
            font=ctk.CTkFont(size=12)
        )
        enrollment_label.pack()
        
        # Financial Summary
        summary_frame = ctk.CTkFrame(self)
        summary_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Resumen Financiero",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        summary_title.pack(pady=10)
        
        # Summary info
        summary_info_frame = ctk.CTkFrame(summary_frame)
        summary_info_frame.pack(fill="x", padx=10, pady=5)
        
        self.total_required_label = ctk.CTkLabel(
            summary_info_frame,
            text="Total Requerido: Cargando...",
            font=ctk.CTkFont(size=12)
        )
        self.total_required_label.pack(side="left", padx=20)
        
        self.total_paid_label = ctk.CTkLabel(
            summary_info_frame,
            text="Total Pagado: Cargando...",
            font=ctk.CTkFont(size=12)
        )
        self.total_paid_label.pack(side="left", padx=20)
        
        self.total_pending_label = ctk.CTkLabel(
            summary_info_frame,
            text="Total Pendiente: Cargando...",
            font=ctk.CTkFont(size=12)
        )
        self.total_pending_label.pack(side="left", padx=20)
        
        # Status
        self.status_label_summary = ctk.CTkLabel(
            summary_info_frame,
            text="Estado: Cargando...",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_label_summary.pack(side="right", padx=20)
        
        # Actions frame
        actions_frame = ctk.CTkFrame(self)
        actions_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.new_payment_button = ctk.CTkButton(
            actions_frame,
            text="Registrar Nuevo Pago",
            command=self.register_payment,
            width=150
        )
        self.new_payment_button.pack(side="left", padx=10, pady=10)
        
        self.process_payment_button = ctk.CTkButton(
            actions_frame,
            text="Procesar Pago Seleccionado",
            command=self.process_payment,
            width=180,
            state="disabled"
        )
        self.process_payment_button.pack(side="left", padx=10, pady=10)
        
        self.refresh_button = ctk.CTkButton(
            actions_frame,
            text="Actualizar",
            command=self.load_payments,
            width=100
        )
        self.refresh_button.pack(side="right", padx=10, pady=10)
        
        # Payments list
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for payments
        self.payments_frame = ctk.CTkScrollableFrame(list_frame)
        self.payments_frame.grid(row=0, column=0, sticky="nsew")
        
        # Status message
        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.grid(row=4, column=0, pady=5)
    
    def load_payments(self):
        """Load payments for the enrollment"""
        try:
            # Get payment summary
            summary = self.payment_service.get_payment_summary(self.enrollment.id)
            
            # Update summary labels
            self.total_required_label.configure(
                text=f"Total Requerido: {summary['total_required']:.2f} XAF"
            )
            self.total_paid_label.configure(
                text=f"Total Pagado: {summary['total_paid']:.2f} XAF"
            )
            self.total_pending_label.configure(
                text=f"Total Pendiente: {summary['total_pending']:.2f} XAF"
            )
            
            # Update status
            if summary['total_pending'] <= 0:
                status_text = "Estado: AL DÍA"
                status_color = "green"
            else:
                status_text = "Estado: PENDIENTE"
                status_color = "orange"
            
            self.status_label_summary.configure(text=status_text, text_color=status_color)
            
            # Get payments list
            self.current_payments = self.payment_service.get_payments_by_enrollment(self.enrollment.id)
            self.display_payments()
            
            self.update_message(f"Se cargaron {len(self.current_payments)} pagos")
            
        except Exception as e:
            self.update_message(f"Error al cargar pagos: {str(e)}", error=True)
    
    def display_payments(self):
        """Display payments in list"""
        # Clear existing widgets
        for widget in self.payments_frame.winfo_children():
            widget.destroy()
        
        if not self.current_payments:
            no_payments_label = ctk.CTkLabel(
                self.payments_frame,
                text="No se encontraron pagos",
                font=ctk.CTkFont(size=14)
            )
            no_payments_label.pack(pady=20)
            return
        
        # Create payment cards
        for i, payment in enumerate(self.current_payments):
            self.create_payment_card(payment, i)
    
    def create_payment_card(self, payment: PaymentModel, index: int):
        """Create a card for a payment"""
        card_frame = ctk.CTkFrame(self.payments_frame)
        card_frame.pack(fill="x", pady=5, padx=5)
        
        # Payment info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Payment details
        amount_text = f"Monto: {payment.amount:.2f} XAF"
        description_text = f"Descripción: {payment.description or 'Sin descripción'}"
        
        if payment.due_date:
            due_date_text = f"Vencimiento: {payment.due_date.strftime('%d/%m/%Y')}"
        else:
            due_date_text = "Vencimiento: No definido"
        
        amount_label = ctk.CTkLabel(
            info_frame,
            text=amount_text,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        amount_label.pack(anchor="w")
        
        description_label = ctk.CTkLabel(
            info_frame,
            text=description_text,
            font=ctk.CTkFont(size=12)
        )
        description_label.pack(anchor="w")
        
        due_date_label = ctk.CTkLabel(
            info_frame,
            text=due_date_text,
            font=ctk.CTkFont(size=11)
        )
        due_date_label.pack(anchor="w")
        
        # Status
        status_color = {
            'PENDING': 'orange',
            'PAID': 'green',
            'OVERDUE': 'red',
            'CANCELLED': 'gray'
        }.get(payment.status, 'black')
        
        status_label = ctk.CTkLabel(
            info_frame,
            text=f"Estado: {payment.status}",
            font=ctk.CTkFont(size=11),
            text_color=status_color
        )
        status_label.pack(anchor="w")
        
        # Payment date if paid
        if payment.payment_date:
            paid_date_text = f"Pagado: {payment.payment_date.strftime('%d/%m/%Y')}"
            paid_date_label = ctk.CTkLabel(
                info_frame,
                text=paid_date_text,
                font=ctk.CTkFont(size=11),
                text_color="green"
            )
            paid_date_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card_frame)
        actions_frame.pack(side="right", padx=10, pady=5)
        
        select_button = ctk.CTkButton(
            actions_frame,
            text="Seleccionar",
            width=80,
            command=lambda p=payment: self.select_payment(p)
        )
        select_button.pack(pady=2)
        
        if payment.status == 'PENDING':
            process_button = ctk.CTkButton(
                actions_frame,
                text="Procesar",
                width=80,
                command=lambda p=payment: self.process_specific_payment(p)
            )
            process_button.pack(pady=2)
        
        # Bind click event
        card_frame.bind("<Button-1>", lambda e, p=payment: self.select_payment(p))
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", lambda e, p=payment: self.select_payment(p))
    
    def select_payment(self, payment: PaymentModel):
        """Select a payment"""
        self.selected_payment = payment
        self.process_payment_button.configure(state="normal")
        self.update_message(f"Seleccionado pago de {payment.amount:.2f} XAF")
    
    def register_payment(self):
        """Register new payment"""
        try:
            # Create simple payment dialog
            dialog = ctk.CTkToplevel(self.winfo_toplevel())
            dialog.title("Registrar Nuevo Pago")
            dialog.geometry("400x300")
            dialog.resizable(False, False)
            
            # Center dialog
            dialog.update_idletasks()
            parent = self.winfo_toplevel()
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
            dialog.geometry(f"400x300+{x}+{y}")
            
            # Make dialog modal
            dialog.transient(self.winfo_toplevel())
            dialog.grab_set()
            
            # Form
            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Amount
            amount_label = ctk.CTkLabel(main_frame, text="Monto:")
            amount_label.pack(anchor="w", pady=5)
            
            amount_entry = ctk.CTkEntry(main_frame, width=300)
            amount_entry.pack(pady=5)
            amount_entry.insert(0, "10000")  # Default amount
            
            # Description
            desc_label = ctk.CTkLabel(main_frame, text="Descripción:")
            desc_label.pack(anchor="w", pady=5)
            
            desc_entry = ctk.CTkEntry(main_frame, width=300)
            desc_entry.pack(pady=5)
            desc_entry.insert(0, "Pago de mensualidad")
            
            # Due date
            due_label = ctk.CTkLabel(main_frame, text="Fecha de Vencimiento (YYYY-MM-DD):")
            due_label.pack(anchor="w", pady=5)
            
            due_entry = ctk.CTkEntry(main_frame, width=300)
            due_entry.pack(pady=5)
            due_entry.insert(0, date.today().strftime("%Y-%m-%d"))
            
            # Payment method
            method_label = ctk.CTkLabel(main_frame, text="Método de Pago:")
            method_label.pack(anchor="w", pady=5)
            
            method_var = ctk.StringVar(value="cash")
            method_combo = ctk.CTkComboBox(
                main_frame, 
                variable=method_var, 
                values=["cash", "transfer", "check"], 
                width=300
            )
            method_combo.pack(pady=5)
            
            # Buttons
            buttons_frame = ctk.CTkFrame(main_frame)
            buttons_frame.pack(fill="x", pady=20)
            
            def save_payment():
                try:
                    amount = float(amount_entry.get())
                    if amount <= 0:
                        raise ValueError("El monto debe ser mayor a 0")
                    
                    description = desc_entry.get().strip()
                    if not description:
                        raise ValueError("La descripción es obligatoria")
                    
                    due_date_str = due_entry.get().strip()
                    if not due_date_str:
                        raise ValueError("La fecha de vencimiento es obligatoria")
                    
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    
                    # Register payment
                    self.payment_service.register_payment(
                        enrollment_id=self.enrollment.id,
                        amount=amount,
                        description=description,
                        due_date=due_date,
                        payment_method=method_var.get()
                    )
                    
                    messagebox.showinfo("Éxito", "Pago registrado exitosamente")
                    dialog.destroy()
                    self.load_payments()
                    
                except ValueError as e:
                    messagebox.showerror("Error de Validación", str(e))
                except Exception as e:
                    messagebox.showerror("Error", f"Error al registrar pago: {str(e)}")
            
            save_button = ctk.CTkButton(
                buttons_frame,
                text="Guardar",
                command=save_payment,
                width=100
            )
            save_button.pack(side="left", padx=10)
            
            cancel_button = ctk.CTkButton(
                buttons_frame,
                text="Cancelar",
                command=dialog.destroy,
                width=100
            )
            cancel_button.pack(side="right", padx=10)
            
            dialog.wait_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir formulario de pago: {str(e)}")
    
    def process_payment(self):
        """Process selected payment"""
        if not self.selected_payment:
            messagebox.showwarning("Advertencia", "Seleccione un pago para procesar")
            return
        
        self.process_specific_payment(self.selected_payment)
    
    def process_specific_payment(self, payment: PaymentModel):
        """Process a specific payment"""
        if payment.status != 'PENDING':
            messagebox.showwarning("Advertencia", "Solo se pueden procesar pagos pendientes")
            return
        
        try:
            # Create payment processing dialog
            dialog = ctk.CTkToplevel(self.winfo_toplevel())
            dialog.title("Procesar Pago")
            dialog.geometry("400x250")
            dialog.resizable(False, False)
            
            # Center dialog
            dialog.update_idletasks()
            parent = self.winfo_toplevel()
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (250 // 2)
            dialog.geometry(f"400x250+{x}+{y}")
            
            # Make dialog modal
            dialog.transient(self.winfo_toplevel())
            dialog.grab_set()
            
            # Form
            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Payment info
            info_label = ctk.CTkLabel(
                main_frame,
                text=f"Procesar pago de {payment.amount:.2f} XAF",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            info_label.pack(pady=10)
            
            desc_label = ctk.CTkLabel(
                main_frame,
                text=f"Descripción: {payment.description or 'Sin descripción'}",
                font=ctk.CTkFont(size=12)
            )
            desc_label.pack(pady=5)
            
            # Amount paid
            amount_label = ctk.CTkLabel(main_frame, text="Monto Pagado:")
            amount_label.pack(anchor="w", pady=5)
            
            amount_entry = ctk.CTkEntry(main_frame, width=300)
            amount_entry.pack(pady=5)
            amount_entry.insert(0, str(payment.amount))  # Default full amount
            
            # Payment method
            method_label = ctk.CTkLabel(main_frame, text="Método de Pago:")
            method_label.pack(anchor="w", pady=5)
            
            method_var = ctk.StringVar(value="cash")
            method_combo = ctk.CTkComboBox(
                main_frame, 
                variable=method_var, 
                values=["cash", "transfer", "check"], 
                width=300
            )
            method_combo.pack(pady=5)
            
            # Buttons
            buttons_frame = ctk.CTkFrame(main_frame)
            buttons_frame.pack(fill="x", pady=20)
            
            def confirm_payment():
                try:
                    amount_paid = float(amount_entry.get())
                    if amount_paid <= 0:
                        raise ValueError("El monto pagado debe ser mayor a 0")
                    
                    # Process payment
                    success = self.payment_service.process_payment(
                        payment_id=payment.id,
                        amount_paid=amount_paid,
                        payment_method=method_var.get()
                    )
                    
                    if success:
                        messagebox.showinfo("Éxito", "Pago procesado exitosamente")
                        dialog.destroy()
                        self.load_payments()
                    else:
                        messagebox.showerror("Error", "No se pudo procesar el pago")
                    
                except ValueError as e:
                    messagebox.showerror("Error de Validación", str(e))
                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar pago: {str(e)}")
            
            confirm_button = ctk.CTkButton(
                buttons_frame,
                text="Confirmar Pago",
                command=confirm_payment,
                width=120
            )
            confirm_button.pack(side="left", padx=10)
            
            cancel_button = ctk.CTkButton(
                buttons_frame,
                text="Cancelar",
                command=dialog.destroy,
                width=100
            )
            cancel_button.pack(side="right", padx=10)
            
            dialog.wait_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar pago: {str(e)}")
    
    def go_back(self):
        """Go back to enrollments view"""
        try:
            # Ocultar esta vista
            self.grid_remove()
            
            # Mostrar la vista anterior si existe
            if self.previous_view:
                self.previous_view.grid()
            
            # Destruir esta vista después de un breve delay
            self.after(100, self.destroy)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al volver: {str(e)}")
    
    def update_message(self, message: str, error: bool = False):
        """Update message label"""
        color = "red" if error else "green"
        self.message_label.configure(text=message, text_color=color)
        # Clear message after 5 seconds
        if hasattr(self, '_message_timer'):
            self.after_cancel(self._message_timer)
        self._message_timer = self.after(5000, lambda: self.message_label.configure(text=""))