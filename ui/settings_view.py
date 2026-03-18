"""
Settings View - Módulo de configuración del sistema
Gestión de usuarios y configuración del centro educativo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os

from database.repository import user_repo
from config import BASE_DIR


class SettingsView:
    """Vista de configuración del sistema"""
    
    def __init__(self, parent: tk.Frame, config: Dict[str, Any], 
                 user_data: Dict[str, Any], api_client=None):
        self.parent = parent
        self.config = config
        self.user_data = user_data
        self.user_role = self._get_role_name(user_data.get('role_id', 0))
        
        # Estado
        self.current_tab = "usuarios"
        self.selected_user_id = None
        self.usuarios_data = []
        self.centro_config = {}
        
        # API Client (si existe)
        self.api_client = api_client
        
        # Crear UI
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_initial_data()
    
    def _get_role_name(self, role_id: int) -> str:
        """Obtiene nombre del rol desde el repositorio"""
        try:
            # Usar BaseRepository para roles
            from database.repository import BaseRepository
            role_repo = BaseRepository('roles')
            role = role_repo.get_by_id(role_id)
            return role['name'] if role else 'Usuario'
        except:
            return 'Usuario'
    
    def create_widgets(self):
        """Crea todos los widgets"""
        # Header
        self.create_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.parent, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Navegación de pestañas
        self.create_navigation_tabs(main_container)
        
        # Área de contenido
        self.create_content_area(main_container)
        
        # Barra de estado
        self.create_status_bar()
        
        # Activar primera pestaña (después de crear content_frame)
        self.switch_tab("usuarios")
    
    def create_header(self):
        """Crea el header"""
        header = tk.Frame(self.parent, bg='#2c3e50', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header,
            text="⚙️ Configuración del Sistema",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        # Info usuario
        user_info = tk.Label(
            header,
            text=f"👤 {self.user_data.get('username', 'Usuario')} | {self.user_role}",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        user_info.pack(side='right', padx=20, pady=15)
    
    def create_navigation_tabs(self, parent):
        """Crea los botones de navegación"""
        nav_frame = tk.Frame(parent, bg='#34495e', height=40)
        nav_frame.pack(fill='x', pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        # Botones de pestañas
        self.tab_buttons = {}
        tabs = [
            ("usuarios", "👥 Usuarios"),
            ("centro", "🏫 Centro")
        ]
        
        for tab_id, tab_text in tabs:
            btn = tk.Button(
                nav_frame,
                text=tab_text,
                font=('Arial', 11, 'bold'),
                bg='#34495e',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=lambda t=tab_id: self.switch_tab(t)
            )
            btn.pack(side='left', padx=5, pady=5)
            self.tab_buttons[tab_id] = btn
    
    def create_content_area(self, parent):
        """Crea el área de contenido dinámico con scroll"""
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.content_frame = tk.Frame(canvas, bg='white')
        
        self.content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        self.content_canvas_window = canvas.create_window(
            (0, 0), window=self.content_frame, anchor='nw'
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.bind('<Configure>', lambda e: (
            canvas.itemconfig(self.content_canvas_window, width=e.width),
            canvas.itemconfig(self.content_canvas_window, height=e.height)
        ))
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_status_bar(self):
        """Crea la barra de estado"""
        status_frame = tk.Frame(self.parent, bg='#34495e', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Listo",
            font=('Arial', 9),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.status_label.pack(side='left', padx=10, pady=2)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label = tk.Label(
            status_frame,
            text=f"Actualizado: {timestamp}",
            font=('Arial', 9),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.timestamp_label.pack(side='right', padx=10, pady=2)
    
    def switch_tab(self, tab_name: str):
        """Cambia entre pestañas"""
        # Actualizar estado
        self.current_tab = tab_name
        
        # Actualizar apariencia de botones
        for tab_id, btn in self.tab_buttons.items():
            if tab_id == tab_name:
                btn.config(bg='#3498db', relief='sunken')
            else:
                btn.config(bg='#34495e', relief='flat')
        
        # Limpiar y crear contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tab_name == "usuarios":
            self.create_usuarios_content()
        elif tab_name == "centro":
            self.create_centro_content()
        
        self.update_status(f"Vista: {tab_name.capitalize()}")
    
    def create_usuarios_content(self):
        """Crea contenido de pestaña usuarios"""
        # Barra de herramientas
        self.create_usuarios_toolbar()
        
        # Tabla de usuarios
        self.create_usuarios_table()
    
    def create_usuarios_toolbar(self):
        """Crea barra de herramientas de usuarios"""
        toolbar = tk.Frame(self.content_frame, bg='#ecf0f1', height=40)
        toolbar.pack(fill='x', padx=10, pady=(10, 5))
        toolbar.pack_propagate(False)
        
        # Botones
        tk.Button(
            toolbar,
            text="➕ Nuevo Usuario",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=self.on_nuevo_usuario
        ).pack(side='left', padx=5, pady=5)
        
        tk.Button(
            toolbar,
            text="🔄 Refrescar",
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.on_refresh_usuarios
        ).pack(side='left', padx=5, pady=5)
        
        tk.Button(
            toolbar,
            text="👤 Activar/Desactivar",
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            cursor='hand2',
            command=self.on_toggle_usuario_estado
        ).pack(side='left', padx=5, pady=5)
    
    def create_usuarios_table(self):
        """Crea tabla de usuarios"""
        # Frame para tabla
        table_frame = tk.Frame(self.content_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('id', 'username', 'rol', 'estado', 'creado')
        self.usuarios_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.usuarios_tree.heading('id', text='ID')
        self.usuarios_tree.heading('username', text='Username')
        self.usuarios_tree.heading('rol', text='Rol')
        self.usuarios_tree.heading('estado', text='Estado')
        self.usuarios_tree.heading('creado', text='Creado')
        
        self.usuarios_tree.column('id', width=50, anchor='center')
        self.usuarios_tree.column('username', width=150)
        self.usuarios_tree.column('rol', width=120)
        self.usuarios_tree.column('estado', width=100, anchor='center')
        self.usuarios_tree.column('creado', width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=scrollbar.set)
        
        # Eventos
        self.usuarios_tree.bind('<<TreeviewSelect>>', self.on_usuario_select)
        
        # Pack
        self.usuarios_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Cargar datos
        self.populate_usuarios_table()
    
    def populate_usuarios_table(self):
        """Llena la tabla de usuarios"""
        # Limpiar tabla
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        # Insertar usuarios
        for user in self.usuarios_data:
            # Obtener nombre del rol
            rol_name = self._get_role_name(user.get('role_id', 0))
            
            # Formatear estado
            estado = "Activo" if user.get('is_active', 0) else "Inactivo"
            estado_color = "#27ae60" if user.get('is_active', 0) else "#e74c3c"
            
            # Formatear fecha
            creado = user.get('created_at', '')
            if creado:
                try:
                    dt = datetime.strptime(creado, '%Y-%m-%d %H:%M:%S')
                    creado = dt.strftime('%d/%m/%Y')
                except:
                    pass
            
            # Insertar en tabla
            item = self.usuarios_tree.insert('', 'end', values=(
                user.get('id', ''),
                user.get('username', ''),
                rol_name,
                estado,
                creado
            ))
            
            # Color según estado
            if not user.get('is_active', 0):
                self.usuarios_tree.set(item, 'estado', f"❌ {estado}")
            else:
                self.usuarios_tree.set(item, 'estado', f"✅ {estado}")
    
    def create_centro_content(self):
        """Crea contenido de pestaña centro"""
        # Frame principal
        main_frame = tk.Frame(self.content_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🏫 Configuración del Centro",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(fill='x', pady=20)
        
        # Nombre del centro
        tk.Label(
            form_frame,
            text="Nombre del Centro:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w', pady=(0, 5))
        
        self.centro_nombre_entry = tk.Entry(
            form_frame,
            font=('Arial', 11),
            width=50
        )
        self.centro_nombre_entry.pack(fill='x', pady=(0, 20))
        
        # Año académico activo
        tk.Label(
            form_frame,
            text="Año Académico Activo:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w', pady=(0, 5))
        
        self.centro_anio_entry = tk.Entry(
            form_frame,
            font=('Arial', 11),
            width=10
        )
        self.centro_anio_entry.pack(anchor='w', pady=(0, 20))
        
        # Frame de información y botones
        info_button_frame = tk.Frame(main_frame, bg='white')
        info_button_frame.pack(fill='x', pady=20)
        
        # Información de última actualización
        self.centro_info_label = tk.Label(
            info_button_frame,
            text="",
            font=('Arial', 9),
            bg='white',
            fg='#7f8c8d'
        )
        self.centro_info_label.pack(anchor='w', pady=(0, 10))
        
        # Botones
        button_frame = tk.Frame(info_button_frame, bg='white')
        button_frame.pack(fill='x')
        
        tk.Button(
            button_frame,
            text="💾 Guardar Configuración",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=self.on_guardar_centro_config,
            width=20
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="🔄 Restablecer",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            command=self.on_restablecer_centro_config,
            width=15
        ).pack(side='left')
        
        # Cargar datos iniciales
        self.populate_centro_form()
    
    def load_initial_data(self):
        """Carga datos iniciales"""
        self.update_status("Cargando configuración inicial...")
        
        # Cargar usuarios
        self.load_usuarios()
        
        # Cargar configuración del centro
        self.load_centro_config()
        
        self.update_status("Configuración cargada")
    
    def load_usuarios(self):
        """Carga lista de usuarios"""
        try:
            self.usuarios_data = user_repo.get_all()
            if hasattr(self, 'usuarios_tree'):
                self.populate_usuarios_table()
        except Exception as e:
            self.update_status(f"Error cargando usuarios: {str(e)}")
            self.usuarios_data = []
    
    def load_centro_config(self):
        """Carga configuración del centro desde config.json"""
        config_path = BASE_DIR / "config.json"
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.centro_config = data.get('centro', {})
            else:
                # Configuración por defecto
                self.centro_config = {
                    'nombre': 'Centro Educativo',
                    'anio_academico': datetime.now().year
                }
        except Exception as e:
            self.update_status(f"Error cargando configuración: {str(e)}")
            self.centro_config = {}
    
    # Event handlers de usuarios
    def on_usuario_select(self, event):
        """Maneja selección de usuario en tabla"""
        selection = self.usuarios_tree.selection()
        if selection:
            item = selection[0]
            values = self.usuarios_tree.item(item, 'values')
            self.selected_user_id = int(values[0]) if values[0] else None
        else:
            self.selected_user_id = None
    
    def on_nuevo_usuario(self):
        """Abre diálogo para nuevo usuario"""
        self.show_nuevo_usuario_dialog()
    
    def on_refresh_usuarios(self):
        """Refresca lista de usuarios"""
        self.load_usuarios()
        self.update_status("Lista de usuarios actualizada")
    
    def on_toggle_usuario_estado(self):
        """Activa/desactiva usuario seleccionado"""
        if not self.selected_user_id:
            messagebox.showwarning("Selección", "Seleccione un usuario primero")
            return
        
        # Encontrar usuario
        user = None
        for u in self.usuarios_data:
            if u.get('id') == self.selected_user_id:
                user = u
                break
        
        if not user:
            return
        
        # Confirmar
        current_state = "Activo" if user.get('is_active', 0) else "Inactivo"
        new_state = "Inactivo" if user.get('is_active', 0) else "Activo"
        
        result = messagebox.askyesno(
            "Confirmar",
            f"¿Cambiar estado de '{user.get('username')}' de {current_state} a {new_state}?"
        )
        
        if result:
            try:
                # Actualizar en base de datos
                new_active = 0 if user.get('is_active', 0) else 1
                user_repo.update(self.selected_user_id, {'is_active': new_active})
                
                # Recargar datos
                self.load_usuarios()
                self.update_status(f"Usuario {user.get('username')} {new_state.lower()}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el usuario: {str(e)}")
    
    def show_nuevo_usuario_dialog(self):
        """Muestra diálogo para crear nuevo usuario"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Nuevo Usuario")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="👤 Crear Nuevo Usuario",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack(pady=(0, 20))
        
        # Campos
        # Username
        tk.Label(main_frame, text="Username:", font=('Arial', 10), bg='white').pack(anchor='w')
        username_entry = tk.Entry(main_frame, font=('Arial', 10), width=30)
        username_entry.pack(fill='x', pady=(0, 10))
        username_entry.focus()
        
        # Password
        tk.Label(main_frame, text="Password:", font=('Arial', 10), bg='white').pack(anchor='w')
        password_entry = tk.Entry(main_frame, font=('Arial', 10), width=30, show='*')
        password_entry.pack(fill='x', pady=(0, 10))
        
        # Rol
        tk.Label(main_frame, text="Rol:", font=('Arial', 10), bg='white').pack(anchor='w')
        rol_var = tk.StringVar(value="Usuario")
        rol_combo = ttk.Combobox(
            main_frame,
            textvariable=rol_var,
            values=["Directiva", "Secretaria", "Usuario"],
            state='readonly',
            font=('Arial', 10)
        )
        rol_combo.pack(fill='x', pady=(0, 20))
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x')
        
        def crear_usuario():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            rol = rol_var.get()
            
            # Validaciones
            if not username:
                messagebox.showerror("Error", "El username es obligatorio")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "El password debe tener al menos 6 caracteres")
                return
            
            # Verificar username único
            existing = user_repo.get_by_username(username)
            if existing:
                messagebox.showerror("Error", "El username ya existe")
                return
            
            try:
                # Obtener role_id
                from database.repository import BaseRepository
                roles_repo = BaseRepository('roles')
                role_record = roles_repo.find_by('name', rol)[0]
                role_id = role_record['id']
                
                # Hashear password (simple por ahora)
                import hashlib
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                # Crear usuario
                user_data = {
                    'username': username,
                    'password_hash': password_hash,
                    'role_id': role_id,
                    'is_active': 1
                }
                
                user_id = user_repo.create(user_data)
                
                messagebox.showinfo("Éxito", f"Usuario '{username}' creado correctamente")
                dialog.destroy()
                
                # Recargar lista
                self.load_usuarios()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")
        
        tk.Button(
            button_frame,
            text="Crear",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=crear_usuario
        ).pack(side='right', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancelar",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right')
    
    def update_status(self, message: str):
        """Actualiza la barra de estado"""
        self.status_label.config(text=message)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Actualizado: {timestamp}")
    
    def populate_centro_form(self):
        """Llena el formulario con datos actuales"""
        # Cargar desde config.json
        nombre = self.config.get('school_name', 'Centro Educativo')
        anio = self.config.get('academic_year', datetime.now().year)
        
        self.centro_nombre_entry.delete(0, tk.END)
        self.centro_nombre_entry.insert(0, str(nombre))
        
        self.centro_anio_entry.delete(0, tk.END)
        self.centro_anio_entry.insert(0, str(anio))
        
        # Mostrar info de última actualización
        ultima_act = self.centro_config.get('ultima_actualizacion', 'No disponible')
        if ultima_act != 'No disponible':
            try:
                dt = datetime.fromisoformat(ultima_act.replace('Z', '+00:00'))
                ultima_act = dt.strftime('%d/%m/%Y %H:%M:%S')
            except:
                pass
        
        self.centro_info_label.config(text=f"Última actualización: {ultima_act}")
    
    def on_guardar_centro_config(self):
        """Guarda la configuración del centro"""
        nombre = self.centro_nombre_entry.get().strip()
        anio = self.centro_anio_entry.get().strip()
        
        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre del centro es obligatorio")
            return
        
        if not anio.isdigit() or len(anio) != 4:
            messagebox.showerror("Error", "El año académico debe ser un número de 4 dígitos")
            return
        
        anio_num = int(anio)
        if anio_num < 1900 or anio_num > 2100:
            messagebox.showerror("Error", "El año académico debe estar entre 1900 y 2100")
            return
        
        try:
            # Leer config actual
            config_path = BASE_DIR / "config.json"
            config_data = {}
            
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            
            # Actualizar valores
            config_data['school_name'] = nombre
            config_data['academic_year'] = anio_num
            
            # Agregar timestamp de actualización
            config_data['centro'] = {
                'nombre': nombre,
                'anio_academico': anio_num,
                'ultima_actualizacion': datetime.now().isoformat()
            }
            
            # Guardar en config.json
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Actualizar config en memoria
            self.config.update(config_data)
            self.centro_config = config_data.get('centro', {})
            
            # Actualizar UI
            self.populate_centro_form()
            
            # Confirmación
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            self.update_status("Configuración del centro actualizada")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {str(e)}")
    
    def on_restablecer_centro_config(self):
        """Restablece el formulario a los valores guardados"""
        self.populate_centro_form()
        self.update_status("Formulario restablecido")
