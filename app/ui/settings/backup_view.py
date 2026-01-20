"""
Backup view for GES application
Handles system backup and restoration
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Dict, List, Optional
from pathlib import Path
from app.services.backup_service import BackupService


class BackupView:
    """Backup management view"""
    
    def __init__(self, parent):
        self.parent = parent
        self.backup_service = BackupService()
        
        # Data
        self.existing_backups = []
        self.selected_backup = None
        
        self.create_widgets()
        self.load_backups()
    
    def create_widgets(self):
        """Create backup view widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Gestión de Backups",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Create backup section
        create_frame = ctk.CTkFrame(main_frame)
        create_frame.pack(fill="x", pady=(0, 10))
        
        create_title = ctk.CTkLabel(
            create_frame,
            text="Crear Backup",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        create_title.pack(pady=10)
        
        # Backup path selection
        path_frame = ctk.CTkFrame(create_frame)
        path_frame.pack(fill="x", padx=10, pady=5)
        
        path_label = ctk.CTkLabel(path_frame, text="Ubicación del Backup:")
        path_label.pack(anchor="w", padx=5)
        
        path_input_frame = ctk.CTkFrame(path_frame)
        path_input_frame.pack(fill="x", pady=5, padx=5)
        
        self.backup_path_entry = ctk.CTkEntry(path_input_frame, width=400)
        self.backup_path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.browse_button = ctk.CTkButton(
            path_input_frame,
            text="Examinar",
            command=self.browse_backup_path,
            width=80
        )
        self.browse_button.pack(side="right", padx=5)
        
        # Create button
        create_button_frame = ctk.CTkFrame(create_frame)
        create_button_frame.pack(fill="x", padx=10, pady=10)
        
        self.create_button = ctk.CTkButton(
            create_button_frame,
            text="Crear Backup Ahora",
            command=self.create_backup,
            width=150,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.create_button.pack(side="left", padx=5)
        
        # Restore section
        restore_frame = ctk.CTkFrame(main_frame)
        restore_frame.pack(fill="x", pady=(0, 10))
        
        restore_title = ctk.CTkLabel(
            restore_frame,
            text="Restaurar Backup",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        restore_title.pack(pady=10)
        
        # Restore path selection
        restore_path_frame = ctk.CTkFrame(restore_frame)
        restore_path_frame.pack(fill="x", padx=10, pady=5)
        
        restore_path_label = ctk.CTkLabel(restore_path_frame, text="Archivo de Backup:")
        restore_path_label.pack(anchor="w", padx=5)
        
        restore_input_frame = ctk.CTkFrame(restore_path_frame)
        restore_input_frame.pack(fill="x", pady=5, padx=5)
        
        self.restore_path_entry = ctk.CTkEntry(restore_input_frame, width=400)
        self.restore_path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.restore_browse_button = ctk.CTkButton(
            restore_input_frame,
            text="Examinar",
            command=self.browse_restore_file,
            width=80
        )
        self.restore_browse_button.pack(side="right", padx=5)
        
        # Restore button
        restore_button_frame = ctk.CTkFrame(restore_frame)
        restore_button_frame.pack(fill="x", padx=10, pady=10)
        
        self.restore_button = ctk.CTkButton(
            restore_button_frame,
            text="Restaurar Sistema",
            command=self.restore_backup,
            width=150,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.restore_button.pack(side="left", padx=5)
        
        # Existing backups section
        existing_frame = ctk.CTkFrame(main_frame)
        existing_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        existing_title = ctk.CTkLabel(
            existing_frame,
            text="Backups Existentes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        existing_title.pack(pady=10)
        
        # Actions for existing backups
        actions_frame = ctk.CTkFrame(existing_frame)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        self.refresh_button = ctk.CTkButton(
            actions_frame,
            text="Actualizar Lista",
            command=self.load_backups,
            width=120
        )
        self.refresh_button.pack(side="left", padx=5)
        
        self.open_folder_button = ctk.CTkButton(
            actions_frame,
            text="Abrir Carpeta",
            command=self.open_backup_folder,
            width=120
        )
        self.open_folder_button.pack(side="right", padx=5)
        
        # Backups list
        list_frame = ctk.CTkFrame(existing_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create scrollable frame for backups
        self.backups_frame = ctk.CTkScrollableFrame(list_frame)
        self.backups_frame.pack(fill="both", expand=True)
        
        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.pack(pady=5)
    
    def load_backups(self):
        """Load existing backups"""
        try:
            self.existing_backups = self.backup_service.get_existing_backups()
            self.display_backups()
            self.update_status(f"Se encontraron {len(self.existing_backups)} backups")
        except Exception as e:
            self.update_status(f"Error al cargar backups: {str(e)}", error=True)
    
    def display_backups(self):
        """Display existing backups in list"""
        # Clear existing widgets
        for widget in self.backups_frame.winfo_children():
            widget.grid_forget()
        
        if not self.existing_backups:
            no_backups_label = ctk.CTkLabel(
                self.backups_frame,
                text="No se encontraron backups existentes",
                font=ctk.CTkFont(size=14)
            )
            no_backups_label.pack(pady=20)
            return
        
        # Create backup cards
        for i, backup in enumerate(self.existing_backups):
            self.create_backup_card(backup, i)
    
    def create_backup_card(self, backup: Dict, index: int):
        """Create a card for a backup"""
        card_frame = ctk.CTkFrame(self.backups_frame)
        card_frame.pack(fill="x", pady=5, padx=5)
        
        # Backup info
        info_frame = ctk.CTkFrame(card_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Filename and date
        filename_text = f"Archivo: {backup['filename']}"
        date_text = f"Fecha: {backup['backup_date'][:10] if backup['backup_date'] else 'Desconocida'}"
        size_text = f"Tamaño: {backup['size_mb']:.2f} MB"
        version_text = f"Versión: {backup.get('version', 'Desconocida')}"
        
        filename_label = ctk.CTkLabel(
            info_frame,
            text=filename_text,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        filename_label.pack(anchor="w")
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=date_text,
            font=ctk.CTkFont(size=11)
        )
        date_label.pack(anchor="w")
        
        size_label = ctk.CTkLabel(
            info_frame,
            text=size_text,
            font=ctk.CTkFont(size=11)
        )
        size_label.pack(anchor="w")
        
        version_label = ctk.CTkLabel(
            info_frame,
            text=version_text,
            font=ctk.CTkFont(size=11)
        )
        version_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card_frame)
        actions_frame.pack(side="right", padx=10, pady=5)
        
        select_button = ctk.CTkButton(
            actions_frame,
            text="Seleccionar",
            width=80,
            command=lambda b=backup: self.select_backup(b)
        )
        select_button.pack(pady=2)
        
        delete_button = ctk.CTkButton(
            actions_frame,
            text="Eliminar",
            width=80,
            fg_color="red",
            hover_color="darkred",
            command=lambda b=backup: self.delete_backup(b)
        )
        delete_button.pack(pady=2)
        
        # Bind click event
        card_frame.bind("<Button-1>", lambda e, b=backup: self.select_backup(b))
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", lambda e, b=backup: self.select_backup(b))
    
    def select_backup(self, backup: Dict):
        """Select a backup for restoration"""
        self.selected_backup = backup
        self.restore_path_entry.delete(0, 'end')
        self.restore_path_entry.insert(0, backup['path'])
        self.update_status(f"Seleccionado: {backup['filename']}")
    
    def browse_backup_path(self):
        """Browse for backup save location"""
        path = filedialog.askdirectory(
            title="Seleccionar ubicación para backup",
            initialdir=self.backup_path_entry.get()
        )
        if path:
            self.backup_path_entry.delete(0, 'end')
            self.backup_path_entry.insert(0, path)
    
    def browse_restore_file(self):
        """Browse for backup file to restore"""
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de backup",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
            initialdir=self.restore_path_entry.get()
        )
        if path:
            self.restore_path_entry.delete(0, 'end')
            self.restore_path_entry.insert(0, path)
    
    def create_backup(self):
        """Create a new backup"""
        try:
            backup_path = self.backup_path_entry.get().strip()
            if not backup_path:
                raise ValueError("Debe especificar una ubicación para el backup")
            
            self.update_status("Creando backup...")
            self.parent.update()
            
            result = self.backup_service.create_backup(backup_path)
            
            if result['success']:
                messagebox.showinfo(
                    "Backup Creado",
                    f"Backup creado exitosamente:\n\n"
                    f"Archivo: {result['backup_path']}\n"
                    f"Tamaño: {result['file_size_mb']:.2f} MB\n"
                    f"Fecha: {result['backup_date']}"
                )
                
                # Refresh backups list
                self.load_backups()
                self.update_status("Backup creado exitosamente")
            else:
                messagebox.showerror("Error", f"No se pudo crear el backup: {result['error']}")
                self.update_status("Error al crear backup", error=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear backup: {str(e)}")
            self.update_status(f"Error al crear backup: {str(e)}", error=True)
    
    def restore_backup(self):
        """Restore system from backup"""
        try:
            backup_path = self.restore_path_entry.get().strip()
            if not backup_path:
                raise ValueError("Debe seleccionar un archivo de backup")
            
            # Validate backup first
            validation = self.backup_service.validate_backup(backup_path)
            
            if not validation['valid']:
                messagebox.showerror("Error de Validación", validation['error'])
                return
            
            # Show backup details
            metadata = validation.get('metadata', {})
            details_text = f"""
Detalles del Backup:
• Archivo: {Path(backup_path).name}
• Fecha: {metadata.get('backup_date', 'Desconocida')}
• Versión: {metadata.get('version', 'Desconocida')}
• Archivos incluidos: {validation.get('files_count', 0)}
• Tamaño: {validation.get('file_size', 0) / (1024*1024):.2f} MB

¿Está seguro que desea restaurar este backup?
            """
            
            if not messagebox.askyesno("Confirmar Restauración", details_text):
                return
            
            self.update_status("Restaurando sistema...")
            self.parent.update()
            
            # Perform restoration
            result = self.backup_service.confirm_restore(backup_path)
            
            if result['success']:
                messagebox.showinfo(
                    "Restauración Completada",
                    f"Sistema restaurado exitosamente:\n\n"
                    f"Archivos restaurados: {', '.join(result['restored_files'])}\n"
                    f"Fecha: {result['restore_date']}\n\n"
                    "Se recomienda reiniciar la aplicación."
                )
                
                self.update_status("Sistema restaurado exitosamente")
            else:
                messagebox.showerror("Error", f"No se pudo restaurar el backup: {result['error']}")
                self.update_status("Error al restaurar backup", error=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al restaurar backup: {str(e)}")
            self.update_status(f"Error al restaurar backup: {str(e)}", error=True)
    
    def delete_backup(self, backup: Dict):
        """Delete a backup file"""
        try:
            filename = backup['filename']
            
            if not messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro que desea eliminar el backup '{filename}'?\n\n"
                "Esta acción no se puede deshacer."
            ):
                return
            
            success = self.backup_service.delete_backup(backup['path'])
            
            if success:
                self.load_backups()
                self.update_status(f"Backup '{filename}' eliminado")
            else:
                self.update_status("Error al eliminar backup", error=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar backup: {str(e)}")
            self.update_status(f"Error al eliminar backup: {str(e)}", error=True)
    
    def open_backup_folder(self):
        """Open backup folder in file explorer"""
        try:
            import subprocess
            import platform
            
            backup_path = self.backup_path_entry.get().strip()
            if not backup_path:
                # Get default backup path
                from app.services.settings_service import SettingsService
                settings_service = SettingsService()
                settings = settings_service.load_settings()
                backup_path = settings.get('paths.backup_path', str(Path.cwd() / "backups"))
            
            backup_path = Path(backup_path)
            
            if not backup_path.exists():
                backup_path.mkdir(parents=True, exist_ok=True)
            
            if platform.system() == "Windows":
                subprocess.run(f'explorer "{backup_path}"', shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(f'open "{backup_path}"', shell=True)
            else:  # Linux
                subprocess.run(f'xdg-open "{backup_path}"', shell=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta: {str(e)}")
    
    def update_status(self, message: str, error: bool = False):
        """Update status label"""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text=""))
