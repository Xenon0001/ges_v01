import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


# Clases de las secciones
class RegistroProfesores(ttk.Frame):
    """Formulario para dar de alta a un nuevo profesor."""
    def __init__(self, parent):
        super().__init__(parent)
        
        # WInfo: NOTA:
        frm_nota = ttk.Frame(self, style=SECONDARY, height=70)
        frm_nota.pack(fill=X, pady=(0, 6))
        frm_nota.pack_propagate(False)
        frm_nota.grid_propagate(False)
        
        frm_nota.grid_columnconfigure(0,weight=1)
        frm_nota.grid_columnconfigure(1,weight=2)
        
        ttk.Label(frm_nota, text="Nota:", font="-weight bold", anchor="center").grid(row=0, column=0, sticky='sw', padx=(5, 0), pady=(5, 0))
        ttk.Label(frm_nota, text="Algunos campos no son obligatorios como el campo email y materias a impartir ya que pueden ser modificados posteriormente.", 
                  justify='left', anchor="center", background='gray21', style='secondary').grid(row=1, column=0, columnspan=2, sticky='sw', padx=(5, 0), ipadx=3, ipady=3, pady=5)
        
        # Frame para los campos del formulario
        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(fill=BOTH, expand=True)
        self.form_frame.pack_propagate(False)
        self.form_frame.grid_propagate(False)
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_rowconfigure(1, weight=1)
        
        self.datos_personales()
        self.contacto()
        self.info_academica()
        self.botones_from()
    
    def datos_personales(self):
        # Datos Personales
        form_frame = ttk.Frame(self.form_frame)
        form_frame.grid(row=0, column=0, sticky=NSEW)
        
        ttk.Label(form_frame, text="Datos Personales", bootstyle=INFO).pack(anchor=W)
        ttk.Label(form_frame, text="Nombre:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Apellidos:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Identificación (DNI/NIE):").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Fecha de Nacimiento:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        
    # Campos de Contacto
    def contacto(self):
        form_frame =ttk.Frame(self.form_frame)
        form_frame.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))
        
        ttk.Label(form_frame, text="Contacto", bootstyle=INFO).pack(anchor=W)
        ttk.Label(form_frame, text="Email:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Teléfono:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Dirección:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        

    # Información Académica
    def info_academica(self):
        form_frame = ttk.Frame(self.form_frame)
        form_frame.grid(row=1, column=0, sticky=NSEW, padx=(0, 5), pady=5)
        
        ttk.Label(form_frame, text="Información Académica", bootstyle=INFO).pack(anchor=W)
        ttk.Label(form_frame, text="Nivel de Estudios:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Especialidad:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
        ttk.Label(form_frame, text="Materias a Impartir:").pack(anchor=W, pady=(5,0))
        ttk.Entry(form_frame, width=50).pack(fill=X)
    
    def botones_from(self):
        form_frame = ttk.Frame(self.form_frame)
        form_frame.grid(row=1, column=1, sticky=NSEW, padx=(5, 0), pady=5)
        
        ttk.Button(form_frame, text="Guardar", bootstyle=SUCCESS, width=30, command=self.guardar_profesor).grid(row=0, column=0, sticky=SE, padx=(0, 5))
        ttk.Button(form_frame, text="Resetear", bootstyle=SUCCESS, width=30, command=self.guardar_profesor).grid(row=0, column=1, sticky=SE)
        
        ttk.Button(form_frame, text="<", bootstyle=SUCCESS, width=30, command=self.guardar_profesor).grid(row=2, column=0, sticky=SE, pady=5, padx=(0, 5))
        ttk.Button(form_frame, text=">", bootstyle=SUCCESS, width=30, command=self.guardar_profesor).grid(row=2, column=1, sticky=SE, pady=5)
        ttk.Button(form_frame, text="Editar Información", bootstyle=SUCCESS, command=self.guardar_profesor).grid(row=3, column=0, sticky=NSEW, columnspan=2)
        
    def guardar_profesor(self):
        """Maneja la lógica de guardar un nuevo profesor.
        Aquí se conectaría con la base de datos."""
        try:
            # Aquí iría el código para guardar los datos.
            # Por ahora, solo mostramos un mensaje.
            Messagebox.show_info("Guardar", "Profesor registrado exitosamente.")
        except Exception as e:
            Messagebox.show_error("Error al Guardar", f"Ocurrió un error al guardar los datos: {e}")