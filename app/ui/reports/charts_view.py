"""
Charts view for GES application
Handles data visualization and charts display
"""

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import base64
from typing import Optional, Dict, List
from app.services.report_service import ReportService
from app.services.school_service import SchoolService


class ChartsView(ctk.CTkFrame):
    """Charts and visualization view"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        
        self.report_service = ReportService()
        self.school_service = SchoolService()
        
        # Data
        self.academic_years = []
        self.available_charts = []
        self.current_chart_image = None
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create charts view widgets"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Gráficas y Reportes",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Controls frame
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Academic year selector
        year_frame = ctk.CTkFrame(controls_frame)
        year_frame.pack(fill="x", padx=10, pady=5)
        
        year_label = ctk.CTkLabel(year_frame, text="Año Académico:")
        year_label.pack(side="left", padx=5)
        
        self.year_var = ctk.StringVar()
        self.year_combo = ctk.CTkComboBox(year_frame, variable=self.year_var, width=300)
        self.year_combo.pack(side="left", padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.on_year_changed())
        
        # Chart selector
        chart_frame = ctk.CTkFrame(controls_frame)
        chart_frame.pack(fill="x", padx=10, pady=5)
        
        chart_label = ctk.CTkLabel(chart_frame, text="Tipo de Gráfica:")
        chart_label.pack(side="left", padx=5)
        
        self.chart_var = ctk.StringVar()
        self.chart_combo = ctk.CTkComboBox(chart_frame, variable=self.chart_var, width=300)
        self.chart_combo.pack(side="left", padx=5)
        self.chart_combo.bind("<<ComboboxSelected>>", lambda e: self.generate_chart())
        
        # Generate button
        self.generate_button = ctk.CTkButton(
            chart_frame,
            text="Generar Gráfica",
            command=self.generate_chart,
            width=120
        )
        self.generate_button.pack(side="left", padx=10)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            chart_frame,
            text="Actualizar Datos",
            command=self.refresh_data,
            width=100
        )
        self.refresh_button.pack(side="right", padx=10)
        
        # Chart display area
        chart_display_frame = ctk.CTkFrame(self)
        chart_display_frame.pack(fill="both", expand=True)
        
        # Chart title
        self.chart_title_label = ctk.CTkLabel(
            chart_display_frame,
            text="Seleccione una gráfica para generar",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.chart_title_label.pack(pady=10)
        
        # Chart image area
        self.chart_frame = ctk.CTkFrame(chart_display_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder label
        self.placeholder_label = ctk.CTkLabel(
            self.chart_frame,
            text="Las gráficas aparecerán aquí",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.placeholder_label.pack(expand=True)
        
        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.pack(pady=5)
    
    def load_data(self):
        """Load initial data"""
        try:
            # Load academic years
            self.academic_years = self.school_service.get_academic_years()
            year_options = [ay.name for ay in self.academic_years]
            if year_options:
                self.year_combo.configure(values=year_options)
                self.year_combo.set(year_options[0])
            
            # Load available charts
            self.available_charts = self.report_service.get_available_charts()
            chart_options = [chart['name'] for chart in self.available_charts]
            if chart_options:
                self.chart_combo.configure(values=chart_options)
                self.chart_combo.set(chart_options[0])
            
            self.update_status("Datos cargados exitosamente")
            
        except Exception as e:
            self.update_status(f"Error al cargar datos: {str(e)}", error=True)
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_data()
        self.clear_chart()
        self.update_status("Datos actualizados")
    
    def on_year_changed(self):
        """Handle academic year change"""
        self.clear_chart()
        self.update_status("Año académico cambiado")
    
    def generate_chart(self):
        """Generate selected chart"""
        try:
            # Get selected academic year
            year_name = self.year_var.get()
            academic_year_id = None
            
            if year_name:
                for ay in self.academic_years:
                    if ay.name == year_name:
                        academic_year_id = ay.id
                        break
            
            # Get selected chart
            chart_name = self.chart_var.get()
            chart_id = None
            
            for chart in self.available_charts:
                if chart['name'] == chart_name:
                    chart_id = chart['id']
                    break
            
            if not chart_id:
                raise ValueError("Seleccione una gráfica válida")
            
            # Update status
            self.update_status("Generando gráfica...")
            self.parent.update()
            
            # Generate chart
            chart_image_base64 = self.report_service.generate_chart(chart_id, academic_year_id)
            
            if chart_image_base64:
                self.display_chart(chart_image_base64, chart_name)
                self.update_status(f"Gráfica '{chart_name}' generada exitosamente")
            else:
                self.clear_chart()
                self.update_status("No se pudo generar la gráfica", error=True)
            
        except Exception as e:
            self.clear_chart()
            self.update_status(f"Error al generar gráfica: {str(e)}", error=True)
    
    def display_chart(self, image_base64: str, chart_name: str):
        """Display chart image"""
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Clear previous chart
            self.clear_chart()
            
            # Update title
            self.chart_title_label.configure(text=chart_name)
            
            # Create image label
            self.chart_image_label = ctk.CTkLabel(self.chart_frame, image=photo)
            self.chart_image_label.image = photo  # Keep reference
            self.chart_image_label.pack(expand=True)
            
            # Store current image
            self.current_chart_image = photo
            
        except Exception as e:
            print(f"Error displaying chart: {e}")
            self.clear_chart()
    
    def clear_chart(self):
        """Clear current chart"""
        # Clear placeholder
        if hasattr(self, 'placeholder_label'):
            self.placeholder_label.pack_forget()
        
        # Clear chart image
        if hasattr(self, 'chart_image_label'):
            self.chart_image_label.grid_forget()
            delattr(self, 'chart_image_label')
        
        # Reset title
        self.chart_title_label.configure(text="Seleccione una gráfica para generar")
        
        # Show placeholder again
        self.placeholder_label.pack(expand=True)
        
        self.current_chart_image = None
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text=""))
    
    def get_chart_description(self) -> str:
        """Get description of currently selected chart"""
        chart_name = self.chart_var.get()
        for chart in self.available_charts:
            if chart['name'] == chart_name:
                return chart['description']
        return ""
