import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox



class GestionAsignaturas(ttk.Frame):
    """Interfaz para la gestión de asignaturas, horarios y carga docente."""
    def __init__(self, parent):
        super().__init__(parent)
        self.inicializar_gestion()
        
    def inicializar_gestion(self):
        ttk.Label(self, text="Gestión de Asignaturas", font="-weight bold").pack(pady=10)
        ttk.Label(self, text="Aquí se gestionarán los horarios y la carga docente de los profesores.", wraplength=400).pack(padx=20, pady=10)
        
        # Ejemplo de una sección de gestión
        gestion_frame = ttk.Frame(self, padding=10, bootstyle=LIGHT)
        gestion_frame.pack(fill=X, padx=20, pady=10)
        
        ttk.Label(gestion_frame, text="Asignar Asignatura a Profesor:").pack(anchor=W, pady=(0, 5))
        ttk.Label(gestion_frame, text="Profesor:").pack(anchor=W, pady=(5, 0))
        ttk.Combobox(gestion_frame, values=["Juan Pérez", "María Gómez", "Carlos Ruiz"]).pack(fill=X)
        
        ttk.Label(gestion_frame, text="Asignatura:").pack(anchor=W, pady=(5, 0))
        ttk.Combobox(gestion_frame, values=["Cálculo", "Programación", "Redes"]).pack(fill=X)
        
        ttk.Button(gestion_frame, text="Asignar", bootstyle=SUCCESS).pack(pady=10)