import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *

import os
from tkinter import PhotoImage




class MainInfoEstudent(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, bootstyle="secondary", text='Informe')
        
        
        self.sinseleccion()
    
    # Si no se seleccionó información previa de estudiante
    def sinseleccion(self):
        BASE_DIR = os.path.dirname(__file__) ###> Debo pasarlo a utils pues pienso reutilizarlo
        icon_path = os.path.join(BASE_DIR, "..", "..", "assets", "icons", "iconest.png")
        
        frm_nota = ttk.Frame(self)
        frm_nota.pack(expand=True, fill=BOTH)
        frm_nota.pack_propagate(False)
        frm_nota.grid_propagate(False)
        
        iconvacio = PhotoImage(file=icon_path)
        
        nota = ttk.Label(frm_nota, image=iconvacio, text='Selecciona Estudiante', compound=TOP)
        nota.image = iconvacio # Guardo una referencia de la imagen para evitar que se borre cuando se acabe la función [Aprendí algo nuevo :)]
        nota.pack(expand=True)