"""
Reports view for GES application
Main reports container with charts and history tabs

reports_view.py - Corregido
"""
import customtkinter as ctk
from app.ui.reports.charts_view import ChartsView
from app.ui.reports.history_view import HistoryView


class ReportsView(ctk.CTkFrame):
    """Main reports view container"""
    
    def __init__(self, parent):
        super().__init__(parent)
        # NO usar pack aquí
        # self.pack(fill="both", expand=True)
        
        self.current_view = None
        
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create reports view with tabs"""
        # Create tabview
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create tabs
        charts_tab = self.notebook.add("Gráficas")
        history_tab = self.notebook.add("Historial Académico")
        
        # Create views for each tab
        self.charts_view = ChartsView(charts_tab)
        self.history_view = HistoryView(history_tab)
