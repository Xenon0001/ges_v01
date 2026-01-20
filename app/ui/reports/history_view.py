"""
History view for GES application
Handles academic history generation and management
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Optional, Dict, List
from app.services.academic_history_service import AcademicHistoryService
from app.services.school_service import SchoolService


class HistoryView:
    """Academic history management view"""
    
    def __init__(self, parent):
        self.parent = parent
        self.history_service = AcademicHistoryService()
        self.school_service = SchoolService()
        
        # Data
        self.academic_years = []
        self.existing_histories = []
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create history view widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Historial Académico",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_generate_tab()
        self.create_manage_tab()
        
        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.pack(pady=5)
    
    def create_generate_tab(self):
        """Create history generation tab"""
        generate_tab = self.notebook.add("Generar Historial")
        
        # Instructions
        instructions_frame = ctk.CTkFrame(generate_tab)
        instructions_frame.pack(fill="x", pady=(0, 10))
        
        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text="Genera un historial académico completo para un año académico específico.",
            font=ctk.CTkFont(size=12)
        )
        instructions_label.pack(pady=10)
        
        # Year selection
        year_frame = ctk.CTkFrame(generate_tab)
        year_frame.pack(fill="x", pady=(0, 10))
        
        year_label = ctk.CTkLabel(year_frame, text="Año Académico:")
        year_label.pack(anchor="w", padx=10)
        
        self.year_var = ctk.StringVar()
        self.year_combo = ctk.CTkComboBox(year_frame, variable=self.year_var, width=400)
        self.year_combo.pack(pady=5, padx=10)
        
        # Check existing history
        check_frame = ctk.CTkFrame(year_frame)
        check_frame.pack(fill="x", padx=10, pady=5)
        
        self.check_button = ctk.CTkButton(
            check_frame,
            text="Verificar si existe historial",
            command=self.check_history_exists,
            width=200
        )
        self.check_button.pack(side="left", padx=5)
        
        self.history_status_label = ctk.CTkLabel(check_frame, text="")
        self.history_status_label.pack(side="left", padx=10)
        
        # Generate button
        generate_frame = ctk.CTkFrame(generate_tab)
        generate_frame.pack(fill="x", pady=(0, 10))
        
        self.generate_button = ctk.CTkButton(
            generate_frame,
            text="Generar Historial Académico",
            command=self.generate_history,
            width=200,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.generate_button.pack(pady=10)
        
        # Preview area
        preview_frame = ctk.CTkFrame(generate_tab)
        preview_frame.pack(fill="both", expand=True)
        
        preview_title = ctk.CTkLabel(
            preview_frame,
            text="Vista Previa del Historial",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        preview_title.pack(pady=10)
        
        self.preview_text = ctk.CTkTextbox(preview_frame, height=300)
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Instructions text
        instructions_text = """
El historial académico incluirá:

📁 Estructura de archivos:
   • estudiantes.json - Datos básicos de estudiantes
   • matriculas.json - Estado de matrículas
   • pagos.json - Resumen financiero
   • resumen.json - Totales y estadísticas

📊 Datos incluidos:
   • Información personal de estudiantes
   • Detalles de matrículas por grado
   • Estado completo de pagos
   • Resumen estadístico anual

💾 Ubicación:
   • Se guardará en la carpeta 'historial/'
   • Formato: <Centro>_<Año>/
   • Compatible con sistema offline
        """
        
        self.preview_text.insert("0.0", instructions_text)
        self.preview_text.configure(state="disabled")
    
    def create_manage_tab(self):
        """Create history management tab"""
        manage_tab = self.notebook.add("Gestionar Historiales")
        
        # Instructions
        instructions_frame = ctk.CTkFrame(manage_tab)
        instructions_frame.pack(fill="x", pady=(0, 10))
        
        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text="Historiales académicos generados anteriormente.",
            font=ctk.CTkFont(size=12)
        )
        instructions_label.pack(pady=10)
        
        # History list
        list_frame = ctk.CTkFrame(manage_tab)
        list_frame.pack(fill="both", expand=True)
        
        # List header
        list_header = ctk.CTkFrame(list_frame)
        list_header.pack(fill="x", padx=10, pady=5)
        
        headers = ["Año Académico", "Estudiantes", "Matrículas", "Total Pagado", "Fecha"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                list_header,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150
            )
            header_label.grid(row=0, column=i, padx=5, pady=5)
        
        # Scrollable frame for history items
        self.history_scroll_frame = ctk.CTkScrollableFrame(list_frame)
        self.history_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Actions frame
        actions_frame = ctk.CTkFrame(manage_tab)
        actions_frame.pack(fill="x", pady=10)
        
        self.refresh_button = ctk.CTkButton(
            actions_frame,
            text="Actualizar Lista",
            command=self.refresh_histories,
            width=120
        )
        self.refresh_button.pack(side="left", padx=10)
        
        self.open_folder_button = ctk.CTkButton(
            actions_frame,
            text="Abrir Carpeta Historial",
            command=self.open_history_folder,
            width=150
        )
        self.open_folder_button.pack(side="left", padx=10)
    
    def load_data(self):
        """Load initial data"""
        try:
            # Load academic years
            self.academic_years = self.school_service.get_academic_years()
            year_options = [ay.name for ay in self.academic_years]
            if year_options:
                self.year_combo.configure(values=year_options)
                self.year_combo.set(year_options[0])
            
            # Load existing histories
            self.refresh_histories()
            
            self.update_status("Datos cargados exitosamente")
            
        except Exception as e:
            self.update_status(f"Error al cargar datos: {str(e)}", error=True)
    
    def refresh_histories(self):
        """Refresh existing histories list"""
        try:
            self.existing_histories = self.history_service.get_existing_histories()
            self.display_histories()
            self.update_status(f"Se encontraron {len(self.existing_histories)} historiales")
        except Exception as e:
            self.update_status(f"Error al cargar historiales: {str(e)}", error=True)
    
    def display_histories(self):
        """Display existing histories in list"""
        # Clear existing items
        for widget in self.history_scroll_frame.winfo_children():
            widget.grid_forget()
        
        if not self.existing_histories:
            no_histories_label = ctk.CTkLabel(
                self.history_scroll_frame,
                text="No se encontraron historiales académicos",
                font=ctk.CTkFont(size=14)
            )
            no_histories_label.pack(pady=20)
            return
        
        # Display each history
        for i, history in enumerate(self.existing_histories):
            self.create_history_item(history, i)
    
    def create_history_item(self, history: Dict, row: int):
        """Create a history item row"""
        summary = history.get('summary', {})
        totals = summary.get('totals', {})
        academic_year = summary.get('academic_year', {})
        
        # Extract data
        year_name = academic_year.get('name', 'Desconocido')
        students_count = totals.get('total_students', 0)
        enrollments_count = totals.get('total_enrollments', 0)
        total_paid = totals.get('total_paid', 0)
        generation_date = summary.get('generation_date', 'Desconocido')
        
        # Format date
        try:
            from datetime import datetime
            if generation_date != 'Desconocido':
                date_obj = datetime.fromisoformat(generation_date.replace('Z', '+00:00'))
                generation_date = date_obj.strftime('%d/%m/%Y')
        except:
            pass
        
        # Create row frame
        row_frame = ctk.CTkFrame(self.history_scroll_frame)
        row_frame.pack(fill="x", pady=2)
        
        # Add data labels
        labels = [
            year_name,
            str(students_count),
            str(enrollments_count),
            f"{total_paid:,.0f} XAF",
            generation_date
        ]
        
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(
                row_frame,
                text=label_text,
                width=140,
                anchor="w"
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Add action buttons
        view_button = ctk.CTkButton(
            row_frame,
            text="Ver",
            width=60,
            command=lambda h=history: self.view_history_details(h)
        )
        view_button.grid(row=0, column=5, padx=5, pady=5)
        
        delete_button = ctk.CTkButton(
            row_frame,
            text="Eliminar",
            width=60,
            fg_color="red",
            hover_color="darkred",
            command=lambda h=history: self.delete_history(h)
        )
        delete_button.grid(row=0, column=6, padx=5, pady=5)
    
    def check_history_exists(self):
        """Check if history exists for selected year"""
        try:
            year_name = self.year_var.get()
            academic_year_id = None
            
            for ay in self.academic_years:
                if ay.name == year_name:
                    academic_year_id = ay.id
                    break
            
            if not academic_year_id:
                self.history_status_label.configure(text="Seleccione un año válido", text_color="red")
                return
            
            exists = self.history_service.history_exists(academic_year_id)
            
            if exists:
                self.history_status_label.configure(
                    text="✅ El historial ya existe para este año", 
                    text_color="orange"
                )
                self.generate_button.configure(
                    text="Regenerar Historial (Sobreescribir)",
                    fg_color="orange"
                )
            else:
                self.history_status_label.configure(
                    text="✅ No existe historial para este año", 
                    text_color="green"
                )
                self.generate_button.configure(
                    text="Generar Historial Académico",
                    fg_color="green"
                )
                
        except Exception as e:
            self.history_status_label.configure(
                text=f"Error al verificar: {str(e)}", 
                text_color="red"
            )
    
    def generate_history(self):
        """Generate academic history"""
        try:
            year_name = self.year_var.get()
            academic_year_id = None
            
            for ay in self.academic_years:
                if ay.name == year_name:
                    academic_year_id = ay.id
                    break
            
            if not academic_year_id:
                raise ValueError("Seleccione un año académico válido")
            
            # Confirm generation
            if not messagebox.askyesno(
                "Confirmar Generación",
                f"¿Está seguro que desea generar el historial académico para '{year_name}'?\n\n"
                "Esto creará archivos JSON con todos los datos del año."
            ):
                return
            
            self.update_status("Generando historial académico...")
            self.parent.update()
            
            # Generate history
            result = self.history_service.generate_academic_history(academic_year_id)
            
            if result['success']:
                messagebox.showinfo(
                    "Éxito",
                    f"Historial académico generado exitosamente:\n\n"
                    f"Carpeta: {result['year_folder']}\n"
                    f"Archivos: {len(result['files_created'])}\n\n"
                    f"Resumen:\n"
                    f"• Estudiantes: {result['summary']['totals']['total_students']}\n"
                    f"• Matrículas: {result['summary']['totals']['total_enrollments']}\n"
                    f"• Total pagado: {result['summary']['totals']['total_paid']:,.0f} XAF"
                )
                
                # Refresh data
                self.refresh_histories()
                self.check_history_exists()
                self.update_status("Historial generado exitosamente")
                
            else:
                messagebox.showerror("Error", f"No se pudo generar el historial: {result['error']}")
                self.update_status("Error al generar historial", error=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar historial: {str(e)}")
            self.update_status(f"Error al generar historial: {str(e)}", error=True)
    
    def view_history_details(self, history: Dict):
        """View details of a specific history"""
        try:
            summary = history.get('summary', {})
            
            # Create details window
            details_window = ctk.CTkToplevel(self.parent)
            details_window.title(f"Detalles del Historial - {history['folder_name']}")
            details_window.geometry("600x500")
            details_window.resizable(False, False)
            
            # Center window
            details_window.update_idletasks()
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (600 // 2)
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (500 // 2)
            details_window.geometry(f"600x500+{x}+{y}")
            
            # Make modal
            details_window.transient(self.parent)
            details_window.grab_set()
            
            # Details display
            main_frame = ctk.CTkFrame(details_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = ctk.CTkLabel(
                main_frame,
                text=f"Historial: {history['folder_name']}",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(pady=(0, 10))
            
            # Details text
            details_text = ctk.CTkTextbox(main_frame, height=350)
            details_text.pack(fill="both", expand=True, pady=10)
            
            # Format details
            details_content = self.format_history_details(summary)
            details_text.insert("0.0", details_content)
            details_text.configure(state="disabled")
            
            # Close button
            close_button = ctk.CTkButton(
                main_frame,
                text="Cerrar",
                command=details_window.destroy,
                width=100
            )
            close_button.pack(pady=10)
            
            details_window.wait_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ver detalles: {str(e)}")
    
    def format_history_details(self, summary: Dict) -> str:
        """Format history summary for display"""
        try:
            content = []
            
            # Academic year info
            academic_year = summary.get('academic_year', {})
            content.append("=== INFORMACIÓN ACADÉMICA ===")
            content.append(f"Año: {academic_year.get('name', 'N/A')}")
            content.append(f"Fecha de generación: {summary.get('generation_date', 'N/A')}")
            content.append("")
            
            # Totals
            totals = summary.get('totals', {})
            content.append("=== TOTALES ===")
            content.append(f"Estudiantes: {totals.get('total_students', 0)}")
            content.append(f"Matrículas: {totals.get('total_enrollments', 0)}")
            content.append(f"Monto requerido: {totals.get('total_required', 0):,.0f} XAF")
            content.append(f"Monto pagado: {totals.get('total_paid', 0):,.0f} XAF")
            content.append(f"Monto pendiente: {totals.get('total_pending', 0):,.0f} XAF")
            content.append(f"Tasa de pago: {totals.get('payment_rate', 0):.1f}%")
            content.append("")
            
            # Grade distribution
            grade_dist = summary.get('grade_distribution', {})
            if grade_dist:
                content.append("=== DISTRIBUCIÓN POR GRADO ===")
                for grade, count in grade_dist.items():
                    content.append(f"{grade}: {count} estudiantes")
                content.append("")
            
            # Payment status
            payment_status = summary.get('payment_status_distribution', {})
            if payment_status:
                content.append("=== ESTADO DE PAGOS ===")
                for status, count in payment_status.items():
                    content.append(f"{status}: {count}")
                content.append("")
            
            # Files
            files = summary.get('files_included', [])
            if files:
                content.append("=== ARCHIVOS INCLUIDOS ===")
                for file in files:
                    content.append(f"• {file}")
            
            return "\n".join(content)
            
        except Exception as e:
            return f"Error al formatear detalles: {str(e)}"
    
    def delete_history(self, history: Dict):
        """Delete a specific history"""
        try:
            summary = history.get('summary', {})
            academic_year = summary.get('academic_year', {})
            year_name = academic_year.get('name', 'desconocido')
            
            if not messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro que desea eliminar el historial de '{year_name}'?\n\n"
                "Esta acción no se puede deshacer."
            ):
                return
            
            # Get academic year ID
            academic_year_id = academic_year.get('id')
            if not academic_year_id:
                raise ValueError("No se pudo identificar el año académico")
            
            success = self.history_service.delete_history(academic_year_id)
            
            if success:
                messagebox.showinfo("Éxito", f"Historial de '{year_name}' eliminado exitosamente")
                self.refresh_histories()
                self.update_status("Historial eliminado")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el historial")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar historial: {str(e)}")
    
    def open_history_folder(self):
        """Open the history folder in file explorer"""
        try:
            import subprocess
            import platform
            
            history_path = self.history_service.history_dir
            
            if platform.system() == "Windows":
                subprocess.run(f'explorer "{history_path}"', shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(f'open "{history_path}"', shell=True)
            else:  # Linux
                subprocess.run(f'xdg-open "{history_path}"', shell=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta: {str(e)}")
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text=""))
