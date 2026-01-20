"""
Settings view for GES application
Handles system configuration and preferences
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Dict, Any
from app.services.settings_service import SettingsService
from app.services.school_service import SchoolService


class SettingsView:
    """Main settings view with tabs"""
    
    def __init__(self, parent):
        self.parent = parent
        self.settings_service = SettingsService()
        self.school_service = SchoolService()
        
        # Current settings
        self.current_settings = {}
        self.academic_years = []
        self.grades = []
        
        self.create_widgets()
        self.load_settings()
    
    def create_widgets(self):
        """Create settings view with tabs"""
        # Create tabview
        self.notebook = ctk.CTkTabview(self.parent)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        general_tab = self.notebook.add("General")
        academic_tab = self.notebook.add("Académico")
        paths_tab = self.notebook.add("Rutas")
        ui_tab = self.notebook.add("Interfaz")
        
        # Create views for each tab
        self.create_general_tab(general_tab)
        self.create_academic_tab(academic_tab)
        self.create_paths_tab(paths_tab)
        self.create_ui_tab(ui_tab)
        
        # Save button at bottom
        save_frame = ctk.CTkFrame(self.parent)
        save_frame.pack(fill="x", padx=10, pady=10)
        
        self.save_button = ctk.CTkButton(
            save_frame,
            text="Guardar Configuración",
            command=self.save_settings,
            width=150,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.save_button.pack(side="left", padx=10)
        
        self.reset_button = ctk.CTkButton(
            save_frame,
            text="Restablecer Valores",
            command=self.reset_settings,
            width=150,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.reset_button.pack(side="right", padx=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(self.parent, text="")
        self.status_label.pack(pady=5)
    
    def create_general_tab(self, parent):
        """Create general settings tab"""
        # School info frame
        school_frame = ctk.CTkFrame(parent)
        school_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            school_frame,
            text="Información del Centro Educativo",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # School name
        name_frame = ctk.CTkFrame(school_frame)
        name_frame.pack(fill="x", pady=5)
        
        name_label = ctk.CTkLabel(name_frame, text="Nombre del Centro:")
        name_label.pack(anchor="w", padx=10)
        
        self.school_name_entry = ctk.CTkEntry(name_frame, width=400)
        self.school_name_entry.pack(pady=5, padx=10)
        
        # School address
        address_frame = ctk.CTkFrame(school_frame)
        address_frame.pack(fill="x", pady=5)
        
        address_label = ctk.CTkLabel(address_frame, text="Dirección:")
        address_label.pack(anchor="w", padx=10)
        
        self.school_address_entry = ctk.CTkEntry(address_frame, width=400)
        self.school_address_entry.pack(pady=5, padx=10)
        
        # School phone
        phone_frame = ctk.CTkFrame(school_frame)
        phone_frame.pack(fill="x", pady=5)
        
        phone_label = ctk.CTkLabel(phone_frame, text="Teléfono:")
        phone_label.pack(anchor="w", padx=10)
        
        self.school_phone_entry = ctk.CTkEntry(phone_frame, width=400)
        self.school_phone_entry.pack(pady=5, padx=10)
        
        # School email
        email_frame = ctk.CTkFrame(school_frame)
        email_frame.pack(fill="x", pady=5)
        
        email_label = ctk.CTkLabel(email_frame, text="Email:")
        email_label.pack(anchor="w", padx=10)
        
        self.school_email_entry = ctk.CTkEntry(email_frame, width=400)
        self.school_email_entry.pack(pady=5, padx=10)
        
        # School website
        website_frame = ctk.CTkFrame(school_frame)
        website_frame.pack(fill="x", pady=5)
        
        website_label = ctk.CTkLabel(website_frame, text="Sitio Web:")
        website_label.pack(anchor="w", padx=10)
        
        self.school_website_entry = ctk.CTkEntry(website_frame, width=400)
        self.school_website_entry.pack(pady=5, padx=10)
    
    def create_academic_tab(self, parent):
        """Create academic settings tab"""
        # Academic settings frame
        academic_frame = ctk.CTkFrame(parent)
        academic_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            academic_frame,
            text="Configuración Académica",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Active academic year
        year_frame = ctk.CTkFrame(academic_frame)
        year_frame.pack(fill="x", pady=5)
        
        year_label = ctk.CTkLabel(year_frame, text="Año Académico Activo:")
        year_label.pack(anchor="w", padx=10)
        
        self.academic_year_var = ctk.StringVar()
        self.academic_year_combo = ctk.CTkComboBox(year_frame, variable=self.academic_year_var, width=400)
        self.academic_year_combo.pack(pady=5, padx=10)
        
        # Default grade
        grade_frame = ctk.CTkFrame(academic_frame)
        grade_frame.pack(fill="x", pady=5)
        
        grade_label = ctk.CTkLabel(grade_frame, text="Grado por Defecto:")
        grade_label.pack(anchor="w", padx=10)
        
        self.default_grade_var = ctk.StringVar()
        self.default_grade_combo = ctk.CTkComboBox(grade_frame, variable=self.default_grade_var, width=400)
        self.default_grade_combo.pack(pady=5, padx=10)
        
        # Enrollment fee
        fee_frame = ctk.CTkFrame(academic_frame)
        fee_frame.pack(fill="x", pady=5)
        
        fee_label = ctk.CTkLabel(fee_frame, text="Cuota de Matrícula por Defecto:")
        fee_label.pack(anchor="w", padx=10)
        
        fee_amount_frame = ctk.CTkFrame(fee_frame)
        fee_amount_frame.pack(pady=5, padx=10)
        
        self.enrollment_fee_entry = ctk.CTkEntry(fee_amount_frame, width=200)
        self.enrollment_fee_entry.pack(side="left", padx=5)
        
        currency_label = ctk.CTkLabel(fee_amount_frame, text="XAF")
        currency_label.pack(side="left", padx=5)
    
    def create_paths_tab(self, parent):
        """Create paths settings tab"""
        # Paths frame
        paths_frame = ctk.CTkFrame(parent)
        paths_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            paths_frame,
            text="Rutas del Sistema",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Backup path
        backup_frame = ctk.CTkFrame(paths_frame)
        backup_frame.pack(fill="x", pady=5)
        
        backup_label = ctk.CTkLabel(backup_frame, text="Carpeta de Backups:")
        backup_label.pack(anchor="w", padx=10)
        
        backup_path_frame = ctk.CTkFrame(backup_frame)
        backup_path_frame.pack(fill="x", pady=5, padx=10)
        
        self.backup_path_entry = ctk.CTkEntry(backup_path_frame, width=350)
        self.backup_path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.backup_browse_button = ctk.CTkButton(
            backup_path_frame,
            text="Examinar",
            command=self.browse_backup_path,
            width=80
        )
        self.backup_browse_button.pack(side="right", padx=5)
        
        # History path
        history_frame = ctk.CTkFrame(paths_frame)
        history_frame.pack(fill="x", pady=5)
        
        history_label = ctk.CTkLabel(history_frame, text="Carpeta de Historial:")
        history_label.pack(anchor="w", padx=10)
        
        history_path_frame = ctk.CTkFrame(history_frame)
        history_path_frame.pack(fill="x", pady=5, padx=10)
        
        self.history_path_entry = ctk.CTkEntry(history_path_frame, width=350)
        self.history_path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.history_browse_button = ctk.CTkButton(
            history_path_frame,
            text="Examinar",
            command=self.browse_history_path,
            width=80
        )
        self.history_browse_button.pack(side="right", padx=5)
        
        # Export path
        export_frame = ctk.CTkFrame(paths_frame)
        export_frame.pack(fill="x", pady=5)
        
        export_label = ctk.CTkLabel(export_frame, text="Carpeta de Exportación:")
        export_label.pack(anchor="w", padx=10)
        
        export_path_frame = ctk.CTkFrame(export_frame)
        export_path_frame.pack(fill="x", pady=5, padx=10)
        
        self.export_path_entry = ctk.CTkEntry(export_path_frame, width=350)
        self.export_path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.export_browse_button = ctk.CTkButton(
            export_path_frame,
            text="Examinar",
            command=self.browse_export_path,
            width=80
        )
        self.export_browse_button.pack(side="right", padx=5)
    
    def create_ui_tab(self, parent):
        """Create UI preferences tab"""
        # UI preferences frame
        ui_frame = ctk.CTkFrame(parent)
        ui_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            ui_frame,
            text="Preferencias de Interfaz",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Theme
        theme_frame = ctk.CTkFrame(ui_frame)
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Tema:")
        theme_label.pack(anchor="w", padx=10)
        
        self.theme_var = ctk.StringVar()
        theme_frame_inner = ctk.CTkFrame(theme_frame)
        theme_frame_inner.pack(pady=5, padx=10)
        
        self.light_radio = ctk.CTkRadioButton(
            theme_frame_inner,
            text="Claro",
            variable=self.theme_var,
            value="light"
        )
        self.light_radio.pack(side="left", padx=10)
        
        self.dark_radio = ctk.CTkRadioButton(
            theme_frame_inner,
            text="Oscuro",
            variable=self.theme_var,
            value="dark"
        )
        self.dark_radio.pack(side="left", padx=10)
        
        self.system_radio = ctk.CTkRadioButton(
            theme_frame_inner,
            text="Sistema",
            variable=self.theme_var,
            value="system"
        )
        self.system_radio.pack(side="left", padx=10)
        
        # Language
        language_frame = ctk.CTkFrame(ui_frame)
        language_frame.pack(fill="x", pady=5)
        
        language_label = ctk.CTkLabel(language_frame, text="Idioma:")
        language_label.pack(anchor="w", padx=10)
        
        self.language_var = ctk.StringVar()
        self.language_combo = ctk.CTkComboBox(
            language_frame, 
            variable=self.language_var, 
            values=["Español", "English", "Français"],
            width=400
        )
        self.language_combo.pack(pady=5, padx=10)
        
        # Auto-save interval
        autosave_frame = ctk.CTkFrame(ui_frame)
        autosave_frame.pack(fill="x", pady=5)
        
        autosave_label = ctk.CTkLabel(autosave_frame, text="Intervalo de Guardado Automático (segundos):")
        autosave_label.pack(anchor="w", padx=10)
        
        self.autosave_entry = ctk.CTkEntry(autosave_frame, width=400)
        self.autosave_entry.pack(pady=5, padx=10)
        
        # Show confirmations
        confirm_frame = ctk.CTkFrame(ui_frame)
        confirm_frame.pack(fill="x", pady=5)
        
        self.show_confirmations_var = ctk.BooleanVar()
        self.show_confirmations_checkbox = ctk.CTkCheckBox(
            confirm_frame,
            text="Mostrar confirmaciones para acciones críticas",
            variable=self.show_confirmations_var
        )
        self.show_confirmations_checkbox.pack(anchor="w", pady=5, padx=10)
    
    def load_settings(self):
        """Load current settings into form"""
        try:
            self.current_settings = self.settings_service.load_settings()
            
            # Load academic years and grades
            self.academic_years = self.school_service.get_academic_years()
            self.grades = self.school_service.get_grades()
            
            # Set up dropdowns
            year_options = ["Ninguno"] + [ay.name for ay in self.academic_years]
            self.academic_year_combo.configure(values=year_options)
            
            grade_options = ["Ninguno"] + [g.name for g in self.grades]
            self.default_grade_combo.configure(values=grade_options)
            
            # Load school info
            school_info = self.current_settings.get('school_info', {})
            self.school_name_entry.delete(0, 'end')
            self.school_name_entry.insert(0, school_info.get('name', ''))
            
            self.school_address_entry.delete(0, 'end')
            self.school_address_entry.insert(0, school_info.get('address', ''))
            
            self.school_phone_entry.delete(0, 'end')
            self.school_phone_entry.insert(0, school_info.get('phone', ''))
            
            self.school_email_entry.delete(0, 'end')
            self.school_email_entry.insert(0, school_info.get('email', ''))
            
            self.school_website_entry.delete(0, 'end')
            self.school_website_entry.insert(0, school_info.get('website', ''))
            
            # Load academic settings
            academic_settings = self.current_settings.get('academic_settings', {})
            
            # Set active academic year
            active_year_id = academic_settings.get('active_academic_year_id')
            if active_year_id:
                for ay in self.academic_years:
                    if ay.id == active_year_id:
                        self.academic_year_combo.set(ay.name)
                        break
            else:
                self.academic_year_combo.set("Ninguno")
            
            # Set default grade
            default_grade_id = academic_settings.get('default_grade_id')
            if default_grade_id:
                for grade in self.grades:
                    if grade.id == default_grade_id:
                        self.default_grade_combo.set(grade.name)
                        break
            else:
                self.default_grade_combo.set("Ninguno")
            
            # Set enrollment fee
            self.enrollment_fee_entry.delete(0, 'end')
            self.enrollment_fee_entry.insert(0, str(academic_settings.get('enrollment_fee', 50000)))
            
            # Load path settings
            path_settings = self.current_settings.get('paths', {})
            
            self.backup_path_entry.delete(0, 'end')
            self.backup_path_entry.insert(0, path_settings.get('backup_path', ''))
            
            self.history_path_entry.delete(0, 'end')
            self.history_path_entry.insert(0, path_settings.get('history_path', ''))
            
            self.export_path_entry.delete(0, 'end')
            self.export_path_entry.insert(0, path_settings.get('export_path', ''))
            
            # Load UI preferences
            ui_preferences = self.current_settings.get('ui_preferences', {})
            
            theme = ui_preferences.get('theme', 'light')
            self.theme_var.set(theme)
            
            language = ui_preferences.get('language', 'es')
            if language == 'es':
                self.language_combo.set("Español")
            elif language == 'en':
                self.language_combo.set("English")
            elif language == 'fr':
                self.language_combo.set("Français")
            else:
                self.language_combo.set("Español")
            
            self.autosave_entry.delete(0, 'end')
            self.autosave_entry.insert(0, str(ui_preferences.get('auto_save_interval', 300)))
            
            self.show_confirmations_var.set(ui_preferences.get('show_confirmations', True))
            
        except Exception as e:
            self.update_status(f"Error al cargar configuración: {str(e)}", error=True)
    
    def save_settings(self):
        """Save current settings"""
        try:
            # Collect school info
            school_info = {
                'name': self.school_name_entry.get().strip(),
                'address': self.school_address_entry.get().strip(),
                'phone': self.school_phone_entry.get().strip(),
                'email': self.school_email_entry.get().strip(),
                'website': self.school_website_entry.get().strip()
            }
            
            # Collect academic settings
            academic_settings = {}
            
            # Get active academic year ID
            year_name = self.academic_year_var.get()
            if year_name and year_name != "Ninguno":
                for ay in self.academic_years:
                    if ay.name == year_name:
                        academic_settings['active_academic_year_id'] = ay.id
                        break
            else:
                academic_settings['active_academic_year_id'] = None
            
            # Get default grade ID
            grade_name = self.default_grade_var.get()
            if grade_name and grade_name != "Ninguno":
                for grade in self.grades:
                    if grade.name == grade_name:
                        academic_settings['default_grade_id'] = grade.id
                        break
            else:
                academic_settings['default_grade_id'] = None
            
            try:
                academic_settings['enrollment_fee'] = float(self.enrollment_fee_entry.get())
            except ValueError:
                academic_settings['enrollment_fee'] = 50000
            
            # Collect path settings
            path_settings = {
                'backup_path': self.backup_path_entry.get().strip(),
                'history_path': self.history_path_entry.get().strip(),
                'export_path': self.export_path_entry.get().strip()
            }
            
            # Collect UI preferences
            ui_preferences = {}
            ui_preferences['theme'] = self.theme_var.get()
            
            language = self.language_var.get()
            if language == "Español":
                ui_preferences['language'] = 'es'
            elif language == "English":
                ui_preferences['language'] = 'en'
            elif language == "Français":
                ui_preferences['language'] = 'fr'
            else:
                ui_preferences['language'] = 'es'
            
            try:
                ui_preferences['auto_save_interval'] = int(self.autosave_entry.get())
            except ValueError:
                ui_preferences['auto_save_interval'] = 300
            
            ui_preferences['show_confirmations'] = self.show_confirmations_var.get()
            
            # Update all settings
            updates = {
                'school_info': school_info,
                'academic_settings': academic_settings,
                'paths': path_settings,
                'ui_preferences': ui_preferences
            }
            
            success = self.settings_service.update_multiple_settings(updates)
            
            if success:
                self.update_status("Configuración guardada exitosamente")
            else:
                self.update_status("Error al guardar configuración", error=True)
                
        except Exception as e:
            self.update_status(f"Error al guardar configuración: {str(e)}", error=True)
    
    def reset_settings(self):
        """Reset settings to defaults"""
        try:
            if messagebox.askyesno(
                "Restablecer Configuración",
                "¿Está seguro que desea restablecer toda la configuración a los valores por defecto?\n\n"
                "Esta acción no se puede deshacer."
            ):
                success = self.settings_service.reset_to_defaults()
                
                if success:
                    self.load_settings()
                    self.update_status("Configuración restablecida exitosamente")
                else:
                    self.update_status("Error al restablecer configuración", error=True)
                    
        except Exception as e:
            self.update_status(f"Error al restablecer configuración: {str(e)}", error=True)
    
    def browse_backup_path(self):
        """Browse for backup directory"""
        path = filedialog.askdirectory(
            title="Seleccionar carpeta de backups",
            initialdir=self.backup_path_entry.get()
        )
        if path:
            self.backup_path_entry.delete(0, 'end')
            self.backup_path_entry.insert(0, path)
    
    def browse_history_path(self):
        """Browse for history directory"""
        path = filedialog.askdirectory(
            title="Seleccionar carpeta de historial",
            initialdir=self.history_path_entry.get()
        )
        if path:
            self.history_path_entry.delete(0, 'end')
            self.history_path_entry.insert(0, path)
    
    def browse_export_path(self):
        """Browse for export directory"""
        path = filedialog.askdirectory(
            title="Seleccionar carpeta de exportación",
            initialdir=self.export_path_entry.get()
        )
        if path:
            self.export_path_entry.delete(0, 'end')
            self.export_path_entry.insert(0, path)
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text=""))
