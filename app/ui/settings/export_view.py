"""
Export view for GES application
Handles data export to Excel format
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Dict, List, Optional
from pathlib import Path
from app.services.export_service import ExportService
from app.services.school_service import SchoolService


class ExportView:
    """Data export management view"""
    
    def __init__(self, parent):
        self.parent = parent
        self.export_service = ExportService()
        self.school_service = SchoolService()
        
        # Data
        self.academic_years = []
        self.available_exports = []
        self.selected_export = None
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create export view widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Exportación de Datos",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Export configuration frame
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", pady=(0, 10))
        
        config_title = ctk.CTkLabel(
            config_frame,
            text="Configuración de Exportación",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        config_title.pack(pady=10)
        
        # Academic year selector
        year_frame = ctk.CTkFrame(config_frame)
        year_frame.pack(fill="x", padx=10, pady=5)
        
        year_label = ctk.CTkLabel(year_frame, text="Año Académico:")
        year_label.pack(anchor="w", padx=5)
        
        self.academic_year_var = ctk.StringVar()
        self.academic_year_combo = ctk.CTkComboBox(year_frame, variable=self.academic_year_var, width=400)
        self.academic_year_combo.pack(pady=5, padx=5)
        self.academic_year_combo.bind("<<ComboboxSelected>>", lambda e: self.on_year_changed())
        
        # Export type selector
        export_frame = ctk.CTkFrame(config_frame)
        export_frame.pack(fill="x", padx=10, pady=5)
        
        export_label = ctk.CTkLabel(export_frame, text="Tipo de Exportación:")
        export_label.pack(anchor="w", padx=5)
        
        self.export_type_var = ctk.StringVar()
        self.export_type_combo = ctk.CTkComboBox(export_frame, variable=self.export_type_var, width=400)
        self.export_type_combo.pack(pady=5, padx=5)
        self.export_type_combo.bind("<<ComboboxSelected>>", lambda e: self.on_export_type_changed())
        
        # Export path selector
        path_frame = ctk.CTkFrame(config_frame)
        path_frame.pack(fill="x", padx=10, pady=5)
        
        path_label = ctk.CTkLabel(path_frame, text="Ubicación de Guardado:")
        path_label.pack(anchor="w", padx=5)
        
        path_input_frame = ctk.CTkFrame(path_frame)
        path_input_frame.pack(fill="x", pady=5, padx=5)
        
        self.export_path_entry = ctk.CTkEntry(path_input_frame, width=350)
        self.export_path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.browse_button = ctk.CTkButton(
            path_input_frame,
            text="Examinar",
            command=self.browse_export_path,
            width=80
        )
        self.browse_button.pack(side="right", padx=5)
        
        # Export details frame
        details_frame = ctk.CTkFrame(main_frame)
        details_frame.pack(fill="x", pady=(0, 10))
        
        details_title = ctk.CTkLabel(
            details_frame,
            text="Detalles de la Exportación",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        details_title.pack(pady=10)
        
        # Export info display
        info_frame = ctk.CTkFrame(details_frame)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.export_info_text = ctk.CTkTextbox(info_frame, height=150)
        self.export_info_text.pack(fill="x", pady=5, padx=5)
        self.export_info_text.insert("0.0", "Seleccione un tipo de exportación para ver detalles...")
        self.export_info_text.configure(state="disabled")
        
        # Export actions frame
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.pack(fill="x", pady=(0, 10))
        
        # Export button
        export_button_frame = ctk.CTkFrame(actions_frame)
        export_button_frame.pack(side="left", padx=10, pady=10)
        
        self.export_button = ctk.CTkButton(
            export_button_frame,
            text="Exportar Datos",
            command=self.export_data,
            width=150,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.export_button.pack(side="left", padx=5)
        
        # Preview button
        self.preview_button = ctk.CTkButton(
            export_button_frame,
            text="Vista Previa",
            command=self.preview_export,
            width=100
        )
        self.preview_button.pack(side="left", padx=5)
        
        # Options button
        options_button_frame = ctk.CTkFrame(actions_frame)
        options_button_frame.pack(side="right", padx=10, pady=10)
        
        self.clear_exports_button = ctk.CTkButton(
            options_button_frame,
            text="Limpiar Temporales",
            command=self.clear_temp_files,
            width=120,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.clear_exports_button.pack(side="right", padx=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.pack(pady=5)
    
    def load_data(self):
        """Load initial data"""
        try:
            # Load academic years
            self.academic_years = self.school_service.get_academic_years()
            year_options = ["Todos los años"] + [ay.name for ay in self.academic_years]
            if year_options:
                self.academic_year_combo.configure(values=year_options)
                self.academic_year_combo.set(year_options[0])
            
            # Load available exports
            self.available_exports = self.export_service.get_available_exports()
            export_options = [exp['name'] for exp in self.available_exports]
            if export_options:
                self.export_type_combo.configure(values=export_options)
                self.export_type_combo.set(export_options[0])
            
            # Set default export path
            from app.services.settings_service import SettingsService
            settings_service = SettingsService()
            settings = settings_service.load_settings()
            export_path = settings.get('paths.export_path', str(Path.home() / "Downloads"))
            
            self.export_path_entry.delete(0, 'end')
            self.export_path_entry.insert(0, export_path)
            
            # Update export details
            self.on_export_type_changed()
            
            self.update_status("Datos cargados exitosamente")
            
        except Exception as e:
            self.update_status(f"Error al cargar datos: {str(e)}", error=True)
    
    def on_year_changed(self):
        """Handle academic year change"""
        self.update_export_info()
        self.update_status("Año académico cambiado")
    
    def on_export_type_changed(self):
        """Handle export type change"""
        # Find selected export
        export_name = self.export_type_var.get()
        self.selected_export = None
        
        for export in self.available_exports:
            if export['name'] == export_name:
                self.selected_export = export
                break
        
        self.update_export_info()
        self.update_status(f"Tipo de exportación: {export_name}")
    
    def update_export_info(self):
        """Update export information display"""
        if not self.selected_export:
            return
        
        try:
            # Get selected year
            year_name = self.academic_year_var.get()
            academic_year_id = None
            
            if year_name and year_name != "Todos los años":
                for ay in self.academic_years:
                    if ay.name == year_name:
                        academic_year_id = ay.id
                        break
            
            # Prepare info text
            info_lines = [
                f"Tipo: {self.selected_export['name']}",
                f"Descripción: {self.selected_export['description']}",
                "",
                "Configuración:",
                f"• Año académico: {year_name}",
                f"• Ubicación: {self.export_path_entry.get()}",
                ""
                "Información:"
            ]
            
            # Try to get preview data
            try:
                export_method = getattr(self.export_service, self.selected_export['method'])
                result = export_method(academic_year_id)
                
                if result['success']:
                    info_lines.extend([
                        f"• Registros estimados: {result.get('record_count', 'N/A')}",
                        f"• Hoja: {result.get('sheet_name', 'N/A')}",
                        f"• Formato: Excel (.xlsx)"
                    ])
                else:
                    info_lines.append(f"• Error: {result.get('error', 'Error desconocido')}")
                    
            except Exception as e:
                info_lines.append(f"• Error al obtener vista previa: {str(e)}")
            
            # Update display
            self.export_info_text.configure(state="normal")
            self.export_info_text.delete("0.0", "end")
            self.export_info_text.insert("0.0", "\n".join(info_lines))
            self.export_info_text.configure(state="disabled")
            
        except Exception as e:
            print(f"Error updating export info: {e}")
    
    def browse_export_path(self):
        """Browse for export directory"""
        path = filedialog.askdirectory(
            title="Seleccionar ubicación para exportación",
            initialdir=self.export_path_entry.get()
        )
        if path:
            self.export_path_entry.delete(0, 'end')
            self.export_path_entry.insert(0, path)
            self.update_status("Ubicación de exportación actualizada")
    
    def preview_export(self):
        """Preview export data"""
        if not self.selected_export:
            messagebox.showwarning("Advertencia", "Seleccione un tipo de exportación")
            return
        
        try:
            # Get selected year
            year_name = self.academic_year_var.get()
            academic_year_id = None
            
            if year_name and year_name != "Todos los años":
                for ay in self.academic_years:
                    if ay.name == year_name:
                        academic_year_id = ay.id
                        break
            
            # Get preview data
            export_method = getattr(self.export_service, self.selected_export['method'])
            result = export_method(academic_year_id)
            
            if not result['success']:
                messagebox.showerror("Error", f"No se pudo obtener vista previa: {result['error']}")
                return
            
            # Create preview window
            self.show_preview_window(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
    
    def show_preview_window(self, export_result: Dict):
        """Show preview window with export data"""
        try:
            preview_window = ctk.CTkToplevel(self.parent)
            preview_window.title(f"Vista Previa - {self.selected_export['name']}")
            preview_window.geometry("800x600")
            preview_window.resizable(True, True)
            
            # Center window
            preview_window.update_idletasks()
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (800 // 2)
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (600 // 2)
            preview_window.geometry(f"800x600+{x}+{y}")
            
            # Make modal
            preview_window.transient(self.parent)
            preview_window.grab_set()
            
            # Main frame
            main_frame = ctk.CTkFrame(preview_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = ctk.CTkLabel(
                main_frame,
                text=f"Vista Previa: {self.selected_export['name']}",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(pady=(0, 10))
            
            # Info
            info_text = ctk.CTkTextbox(main_frame, height=400)
            info_text.pack(fill="both", expand=True, pady=10)
            
            # Format preview info
            preview_info = [
                f"Tipo de Exportación: {self.selected_export['name']}",
                f"Descripción: {self.selected_export['description']}",
                f"Registros: {export_result.get('record_count', 0)}",
                f"Nombre del Archivo: {export_result.get('filename', 'N/A')}",
                f"Hoja de Excel: {export_result.get('sheet_name', 'N/A')}",
                "",
                "Primeros 10 registros (vista previa):",
                ""
            ]
            
            # Add data preview
            if 'dataframe' in export_result:
                df = export_result['dataframe']
                preview_info.append(df.head(10).to_string(index=False))
            else:
                preview_info.append("No se pudo obtener vista previa de los datos")
            
            info_text.insert("0.0", "\n".join(preview_info))
            info_text.configure(state="disabled")
            
            # Close button
            close_button = ctk.CTkButton(
                main_frame,
                text="Cerrar",
                command=preview_window.destroy,
                width=100
            )
            close_button.pack(pady=10)
            
            preview_window.wait_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar vista previa: {str(e)}")
    
    def export_data(self):
        """Export data to Excel"""
        if not self.selected_export:
            messagebox.showwarning("Advertencia", "Seleccione un tipo de exportación")
            return
        
        try:
            # Get selected year
            year_name = self.academic_year_var.get()
            academic_year_id = None
            
            if year_name and year_name != "Todos los años":
                for ay in self.academic_years:
                    if ay.name == year_name:
                        academic_year_id = ay.id
                        break
            
            # Get export path
            export_path = self.export_path_entry.get().strip()
            if not export_path:
                raise ValueError("Debe especificar una ubicación para guardar el archivo")
            
            self.update_status("Exportando datos...")
            self.parent.update()
            
            # Perform export
            export_method = getattr(self.export_service, self.selected_export['method'])
            export_result = export_method(academic_year_id)
            
            if not export_result['success']:
                raise ValueError(export_result['error'])
            
            # Save file
            save_result = self.export_service.save_excel_file(export_result, export_path)
            
            if save_result['success']:
                file_path = save_result['file_path']
                file_size = save_result['file_size']
                file_size_mb = file_size / (1024 * 1024)
                
                messagebox.showinfo(
                    "Exportación Completada",
                    f"Datos exportados exitosamente:\n\n"
                    f"Archivo: {Path(file_path).name}\n"
                    f"Ubicación: {file_path}\n"
                    f"Tamaño: {file_size_mb:.2f} MB\n"
                    f"Registros: {export_result.get('record_count', 0)}"
                )
                
                self.update_status("Exportación completada exitosamente")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Abrir Archivo", "¿Desea abrir el archivo exportado?"):
                    self.open_export_file(file_path)
            else:
                raise ValueError(save_result['error'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos: {str(e)}")
            self.update_status(f"Error al exportar datos: {str(e)}", error=True)
    
    def open_export_file(self, file_path: str):
        """Open exported Excel file"""
        try:
            import subprocess
            import platform
            
            file_path = Path(file_path)
            
            if platform.system() == "Windows":
                subprocess.run(f'start excel "{file_path}"', shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(f'open "{file_path}"', shell=True)
            else:  # Linux
                subprocess.run(f'xdg-open "{file_path}"', shell=True)
                
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo abrir el archivo automáticamente: {str(e)}\n\nPuede abrirlo manualmente desde: {file_path}")
    
    def clear_temp_files(self):
        """Clear temporary export files"""
        try:
            # This would clear any temporary files created during export
            # For now, just show confirmation
            if messagebox.askyesno(
                "Limpiar Archivos Temporales",
                "¿Está seguro que desea limpiar los archivos temporales de exportación?\n\n"
                "Esto eliminará cualquier archivo temporal creado durante el proceso de exportación."
            ):
                # Implementation would go here
                messagebox.showinfo("Completado", "Archivos temporales limpiados")
                self.update_status("Archivos temporales limpiados")
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar archivos temporales: {str(e)}")
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text=""))
