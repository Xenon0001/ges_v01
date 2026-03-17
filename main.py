"""
GES - Sistema de Gestión Escolar
Punto de entrada principal de la aplicación
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import DB_PATH, DEFAULT_PORT
from database.models import DatabaseModels
from ui.login import LoginWindow
from ui.dashboard import DashboardWindow
import tkinter as tk
from tkinter import messagebox


class GESApplication:
    """Aplicación principal GES"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GES")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Configuración
        self.config = self.load_config()
        self.current_user = None
        self.api_client = None  # Se inicializará en modo cliente
        
        # Inicializar base de datos
        self.initialize_database()
        
        # Estado de la aplicación
        self.current_window = None
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_config(self) -> Dict[str, Any]:
        """Carga configuración desde config.json"""
        config_path = Path(__file__).parent / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Configuración por defecto
        default_config = {
            "mode": "normal",  # normal, server, client
            "server_ip": None,
            "port": DEFAULT_PORT,
            "school_name": "Centro Educativo GES",
            "academic_year": 2024
        }
        
        # Guardar configuración por defecto
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Guarda configuración en config.json"""
        config_path = Path(__file__).parent / "config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError:
            messagebox.showerror("Error", "No se pudo guardar la configuración")
    
    def initialize_database(self) -> None:
        """Inicializa la base de datos"""
        try:
            models = DatabaseModels()
            models.initialize_database()
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", 
                              f"No se pudo inicializar la base de datos:\n{str(e)}")
            sys.exit(1)
    
    def show_login(self) -> None:
        """Muestra ventana de login"""
        if self.current_window:
            # Limpiar ventana anterior sin llamar a destroy()
            # ya que LoginWindow no tiene ese método
            try:
                # Limpiar widgets del login anterior
                for widget in self.root.winfo_children():
                    widget.destroy()
            except:
                pass
        
        self.current_window = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, user_data: Dict[str, Any], password: str) -> None:
        try:
            self.current_user = user_data
            self.user_role = self._get_role_name(user_data.get('role_id', 0))
            
            if self.config.get('mode') == 'client':
                from services.api_client import GESApiClient
                self.api_client = GESApiClient(self.config)
                
                try:
                    api_user_data = self.api_client.login(user_data['username'], password)
                    self.current_user = api_user_data
                except Exception as e:
                    messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor:\n{str(e)}")
                    return
            
            self.show_dashboard()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    def _get_role_name(self, role_id: int) -> str:
        """Obtiene nombre del rol desde ID"""
        role_names = {
            1: "Directiva",
            2: "Secretaria", 
            3: "Usuario"
        }
        return role_names.get(role_id, "Usuario")
    
    def show_dashboard(self) -> None:
        """Muestra dashboard principal"""
        if self.current_window:
            # Limpiar ventana anterior sin llamar a destroy()
            # ya que las ventanas no tienen ese método
            try:
                # Limpiar widgets del dashboard anterior
                for widget in self.root.winfo_children():
                    widget.destroy()
            except:
                pass
        
        # En modo cliente, pasar API client al DashboardWindow
        if self.config.get('mode') == 'client':
            self.current_window = DashboardWindow(
                self.root, 
                self.current_user, 
                self.config,
                self.on_logout,
                self.api_client  # ← Nuevo parámetro
            )
        else:
            # Modo normal (comportamiento existente)
            self.current_window = DashboardWindow(
                self.root, 
                self.current_user, 
                self.config,
                self.on_logout
            )
    
    def on_logout(self) -> None:
        """Callback cuando se hace logout"""
        self.current_user = None
        self.show_login()
    
    def run(self) -> None:
        """Inicia la aplicación"""
        # Mostrar login primero
        self.show_login()
        
        # Iniciar loop principal
        self.root.mainloop()


def check_dependencies():
    """Verifica dependencias necesarias"""
    try:
        import tkinter
        import sqlite3
        return True
    except ImportError as e:
        messagebox.showerror("Dependencia Faltante", 
                          f"Falta dependencia requerida:\n{str(e)}")
        return False


def main():
    """Función principal"""
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Crear y ejecutar aplicación
    try:
        app = GESApplication()
        app.run()
    except Exception as e:
        messagebox.showerror("Error Crítico", 
                          f"Error al iniciar GES:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
