import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *


class InfoView(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Boletin Informativo')
        
        self.canvas = ttk.Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=self.canvas.yview)
        
        self.frm_desplazable = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frm_desplazable, anchor='nw', tags='frm_desplazable')

        self.frm_desplazable.bind("<Configure>", self._on_frame_configure)
        
        self.fristinfo('Luis Rafael Eyoma', 'OBIANG AYETEBE', '1º Esba', 'Mª Magadalena Ayetebe', 'A')
        
    def fristinfo(self, nombre, apellido, curso, tutor, clase):
        frm_info = ttk.Frame(self.frm_desplazable, style='secondary')
        frm_info.pack(fill=BOTH)
        frm_info.grid_columnconfigure(0, weight=3)
        frm_info.grid_columnconfigure(1, weight=1)
        frm_info.grid_columnconfigure(2, weight=1)
        
        ttk.Label(frm_info, text='img', font=('arial', 17)).grid(row=4, column=0, rowspan=7, sticky='nsew')
        
        ttk.Label(frm_info, text='Nombre: ').grid(row=0, column=1, sticky=W)
        self.nombre = ttk.Label(frm_info, text=nombre)
        self.nombre.grid(row=1, column=1, sticky=W)
        
        ttk.Label(frm_info, text='Apellido').grid(row=2, column=1, sticky=W)
        self.apellido = ttk.Label(frm_info, text=apellido)
        self.apellido.grid(row=3, column=1, sticky=W)
        
        ttk.Label(frm_info, text='Curso').grid(row=4, column=1, sticky=W)
        self.curso = ttk.Label(frm_info, text=curso)
        self.curso.grid(row=5, column=1, sticky=W)
        
        ttk.Label(frm_info, text='Clase').grid(row=4, column=2, sticky=W)
        self.clase = ttk.Label(frm_info, text=clase)
        self.clase.grid(row=5, column=2, sticky=W)
        
        ttk.Label(frm_info, text='Tutor').grid(row=6, column=1, sticky=W)
        self.turno = ttk.Label(frm_info, text=tutor)
        self.turno.grid(row=7, column=1, sticky=W)
    
    def cambiar_de_vista(self, vista):
        if vista == 'select':
            pass
            
    # Funcion que recalcula el tamaño del scrollbar
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        