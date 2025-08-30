import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .maininfo import MainInfoEstudent
from .infoselect import InfoView
from .select_gui import ListaEstudiantes

class Boletin(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Frame superior para los botones de navegación
        menu_frame = ttk.Frame(self, height=200)
        menu_frame.pack(side=TOP, fill=X)
        
        menu_frame.grid_columnconfigure(0, weight=2)
        menu_frame.grid_columnconfigure(1, weight=1)
        
        # Botones del menu
        """
            ESTRUCTURA DE LA INTERFAZ DEL MENU
            __________________________________________________
            # Col0 (Espacio máximo) | # Col1 (Espacio minimo)|
            ________________________|________________________|
                                    |    [boton] [boton]     |
            [boton]                 |    [boton] [boton]     |
            ________________________|________________________|
        """
        
        ttk.Button(menu_frame, text='Imprimir informe', width=30).grid(row=0, column=1, sticky=E, pady=5)
        ttk.Button(menu_frame, text='Convertir a PDF', width=30).grid(row=1, column=1, sticky=E, pady=(0, 5))
        ttk.Button(menu_frame, text='Convertir a PDF', width=30).grid(row=2, column=1, sticky=E, pady=(0, 5))
        
        ttk.Button(menu_frame, text='Seleccionar alumno', command=lambda: self.select()).grid(row=2, column=0, sticky=W)
        
        self.maininfo = MainInfoEstudent(self)
        self.maininfo.pack(expand=True, fill=BOTH)
        
        self.infoview = InfoView(self)
        # self.infoview.pack(expand=True, fill=BOTH)
    
    def select(self):
        self.selec_est = ListaEstudiantes(self)