"""
Login Window - Ventana de autenticación GES
Diseño profesional e institucional
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any, Optional

from database.repository import user_repo
from database.models import DatabaseModels
from utils.helpers import hash_password


class LoginWindow:
    """Ventana de login profesional"""
    
    def __init__(self, parent: tk.Tk, on_success: Callable[[Dict[str, Any], str], None]):
        self.parent = parent
        self.on_success = on_success
        
        # Configurar ventana principal
        self.setup_window()
        
        # Crear UI
        self.create_widgets()
        
        # Enfocar username
        self.username_entry.focus()
        
        # Bind Enter key
        self.parent.bind('<Return>', lambda e: self.login())
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.parent.title("GES - Sistema de Gestión Escolar")
        self.parent.geometry("400x500")
        self.parent.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar estilo profesional
        self.setup_styles()
        
        # Color de fondo institucional
        self.parent.configure(bg='#f0f4f8')
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.parent.update_idletasks()
        width = self.parent.winfo_width()
        height = self.parent.winfo_height()
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.parent.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configura estilos profesionales"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Estilo para botones principales
        style.configure('Primary.TButton',
                     background='#2c3e50',
                     foreground='white',
                     borderwidth=0,
                     focuscolor='none',
                     font=('Segoe UI', 11, 'bold'))
        style.map('Primary.TButton',
                 background=[('active', '#34495e')])
        
        # Estilo para frames
        style.configure('Card.TFrame',
                     background='white',
                     relief='flat',
                     borderwidth=1)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Header con título
        self.create_header()
        
        # Tarjeta principal de login
        self.create_login_card()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Crea el header con logo y título"""
        header_frame = tk.Frame(self.parent, bg='#f0f4f8', height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="GES",
            font=('Segoe UI', 32, 'bold'),
            fg='#2c3e50',
            bg='#f0f4f8'
        )
        title_label.pack(pady=(20, 5))
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="Sistema de Gestión Escolar",
            font=('Segoe UI', 12),
            fg='#7f8c8d',
            bg='#f0f4f8'
        )
        subtitle_label.pack()
    
    def create_login_card(self):
        """Crea la tarjeta principal de login"""
        # Frame principal (tarjeta)
        card_frame = tk.Frame(self.parent, bg='white', relief='solid', borderwidth=1)
        card_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Espaciado interno
        inner_frame = tk.Frame(card_frame, bg='white')
        inner_frame.pack(pady=30, padx=40, fill='both', expand=True)
        
        # Título de la tarjeta
        card_title = tk.Label(
            inner_frame,
            text="Iniciar Sesión",
            font=('Segoe UI', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        card_title.pack(pady=(0, 25))
        
        # Campo de usuario
        self.create_username_field(inner_frame)
        
        # Campo de contraseña
        self.create_password_field(inner_frame)
        
        # Botón de login
        self.create_login_button(inner_frame)
        
        # Mensaje de ayuda
        self.create_help_message(inner_frame)
    
    def create_username_field(self, parent):
        """Crea el campo de usuario"""
        # Label
        username_label = tk.Label(
            parent,
            text="Usuario:",
            font=('Segoe UI', 10),
            fg='#2c3e50',
            bg='white',
            anchor='w'
        )
        username_label.pack(fill='x', pady=(0, 5))
        
        # Entry
        self.username_entry = tk.Entry(
            parent,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.username_entry.pack(fill='x', pady=(0, 15))
        self.username_entry.configure(insertbackground='#3498db')
    
    def create_password_field(self, parent):
        """Crea el campo de contraseña"""
        # Label
        password_label = tk.Label(
            parent,
            text="Contraseña:",
            font=('Segoe UI', 10),
            fg='#2c3e50',
            bg='white',
            anchor='w'
        )
        password_label.pack(fill='x', pady=(0, 5))
        
        # Entry
        self.password_entry = tk.Entry(
            parent,
            font=('Segoe UI', 11),
            show='•',
            relief='solid',
            borderwidth=1,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.password_entry.pack(fill='x', pady=(0, 20))
        self.password_entry.configure(insertbackground='#3498db')
    
    def create_login_button(self, parent):
        """Crea el botón de login"""
        self.login_button = tk.Button(
            parent,
            text="Iniciar Sesión",
            font=('Segoe UI', 12, 'bold'),
            bg='#2c3e50',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.login,
            height=1
        )
        self.login_button.pack(fill='x', pady=(0, 15))
        
        # Efecto hover
        self.login_button.bind('<Enter>', lambda e: self.login_button.configure(bg='#34495e'))
        self.login_button.bind('<Leave>', lambda e: self.login_button.configure(bg='#2c3e50'))
    
    def create_help_message(self, parent):
        """Crea mensaje de ayuda"""
        help_frame = tk.Frame(parent, bg='white')
        help_frame.pack(fill='x')
        
        help_label = tk.Label(
            help_frame,
            text="Usuario: admin | Contraseña: admin123",
            font=('Segoe UI', 9),
            fg='#7f8c8d',
            bg='white'
        )
        help_label.pack()
    
    def create_footer(self):
        """Crea el footer de la ventana"""
        footer_frame = tk.Frame(self.parent, bg='#f0f4f8', height=60)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Información del sistema
        info_label = tk.Label(
            footer_frame,
            text="© 2024 GES - Sistema de Gestión Escolar",
            font=('Segoe UI', 9),
            fg='#95a5a6',
            bg='#f0f4f8'
        )
        info_label.pack(pady=20)
    
    def validate_inputs(self) -> bool:
        """Valida los campos de entrada"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error de Validación", "El nombre de usuario es obligatorio")
            self.username_entry.focus()
            return False
        
        if len(username) > 50:
            messagebox.showerror("Error de Validación", "El nombre de usuario no puede exceder 50 caracteres")
            self.username_entry.focus()
            return False
        
        if not password:
            messagebox.showerror("Error de Validación", "La contraseña es obligatoria")
            self.password_entry.focus()
            return False
        
        return True
    
    def login(self):
        """Procesa el login"""
        if not self.validate_inputs():
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        try:
            # Buscar usuario
            user = user_repo.get_by_username(username)
            
            if not user:
                messagebox.showerror("Error de Autenticación", 
                                  "Usuario o contraseña incorrectos")
                return
            
            # Verificar contraseña (en MVP, comparación simple)
            # En producción, usar hash_password
            if user['password_hash'] != hash_password(password):
                messagebox.showerror("Error de Autenticación", 
                                  "Usuario o contraseña incorrectos")
                return
            
            # Verificar que esté activo
            if not user['is_active']:
                messagebox.showerror("Error de Autenticación", 
                                  "El usuario está desactivado")
                return
            
            # Login exitoso
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'role_id': user['role_id'],
                'is_active': user['is_active']
            }
            
            # Llamar callback con user_data Y contraseña
            self.on_success(user_data, password)
            
        except Exception:
            messagebox.showerror("Error del Sistema", 
                              "Ocurrió un error al procesar el login. Por favor, intente nuevamente.")
    
    def create_default_admin(self):
        """Crea usuario admin por defecto si no existe"""
        try:
            admin_user = user_repo.get_by_username('admin')
            if not admin_user:
                # Crear usuario admin por defecto
                admin_data = {
                    'username': 'admin',
                    'password_hash': hash_password('admin123'),
                    'role_id': 1,  # Rol de Directiva
                    'is_active': True
                }
                user_repo.create(admin_data)
        except Exception as e:
            print(f"⚠️ Error creando usuario admin por defecto: {e}")


# Función para inicializar usuarios por defecto
def initialize_default_users():
    """Inicializa usuarios por defecto del sistema"""
    try:
        # Verificar si existe el usuario admin
        admin_user = user_repo.get_by_username('admin')
        if not admin_user:
            # Crear usuario admin por defecto
            admin_data = {
                'username': 'admin',
                'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
                'role_id': 1,  # Rol de Directiva
                'is_active': True
            }
            user_repo.create(admin_data)
            print("✅ Usuario admin creado por defecto")
    except Exception as e:
        print(f"⚠️ Error creando usuario admin: {e}")


# La función initialize_default_users() está disponible pero no se ejecuta automáticamente
# Se debe llamar explícitamente cuando se necesite
