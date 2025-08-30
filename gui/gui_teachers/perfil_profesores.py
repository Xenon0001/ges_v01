import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class PerfilProfesor(ttk.Frame):
    """Vista detallada del perfil de un profesor."""
    def __init__(self, parent):
        super().__init__(parent)
        self.inicializar_perfil()

    def inicializar_perfil(self):
        ttk.Label(self, text="Perfil del Profesor", font="-weight bold").pack(pady=10)
        
        # Frame para los datos del perfil
        perfil_frame = ttk.Frame(self)
        perfil_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Datos estáticos para el perfil
        datos_personales = {
            "Nombre": "Juan Pérez",
            "Fecha de Nacimiento": "15/05/1980",
            "DNI": "12345678X",
            "Contacto": "juan.perez@email.com"
        }
        
        info_academica = {
            "Títulos": "Ingeniero de Software, Máster en Ciberseguridad",
            "Especialidad": "Ingeniería de Software"
        }
        
        materias_imparte = {
            "Asignaturas": "Cálculo, Programación",
            "Cursos": "Desarrollo Web Avanzado"
        }
        
        # Crear los campos de información
        self.crear_seccion(perfil_frame, "Datos Personales", datos_personales, INFO)
        self.crear_seccion(perfil_frame, "Información Académica", info_academica, WARNING)
        self.crear_seccion(perfil_frame, "Asignaturas y Cursos", materias_imparte, DANGER)

    def crear_seccion(self, parent_frame, titulo, datos, estilo):
        """Crea una sección de perfil con título y datos."""
        ttk.Label(parent_frame, text=titulo, bootstyle=estilo, font="-weight bold").pack(anchor=W, pady=(10, 5))
        for clave, valor in datos.items():
            ttk.Label(parent_frame, text=f"{clave}: {valor}").pack(anchor=W)