"""
Settings view for GES application
Main settings container with tabs

settings_view.py - Corregido
"""
import customtkinter as ctk
from app.ui.settings.settings_view import SettingsView as SettingsDetailView
from app.ui.settings.backup_view import BackupView
from app.ui.settings.export_view import ExportView


class SettingsView(ctk.CTkFrame):
    """Main settings view container"""
    
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
        """Create settings view with tabs"""
        # Create tabview
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create tabs
        general_tab = self.notebook.add("General")
        backup_tab = self.notebook.add("Backups")
        export_tab = self.notebook.add("Exportación")
        
        # Create views for each tab
        self.settings_detail_view = SettingsDetailView(general_tab)
        self.backup_view = BackupView(backup_tab)
        self.export_view = ExportView(export_tab)