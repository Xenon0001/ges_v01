import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ListaEstudiantes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        frame_search = ttk.Frame(self, height=100)
        self.table_frame = ttk.Frame(self)
        
        # Mostrar en pantalla
        frame_search.pack(fill=X)
        frame_search.pack_propagate(False)
        frame_search.grid_propagate(False)
        
        self.table_frame.pack(expand=True, fill=BOTH, pady=10)
        self.table_frame.pack_propagate(None)
        self.table_frame.grid_propagate(None)
        
        # widget para frame search
        ttk.Label(frame_search, text="Nombre del estudiante", justify=LEFT).grid(row=0, column=0, sticky=W, pady=(20, 5))
        
        self.buscador_est = ttk.Entry(frame_search, width=70, justify=LEFT, show="Nombre")
        self.buscador_est.grid(row=1, column=0, sticky=NSEW, columnspan=2, ipady=4)
        
        option = ['Mañana', 'Tarde']
        
        selec_option = ttk.StringVar(frame_search)
        selec_option.set(option[0])
        
        self.filt_turno = ttk.OptionMenu(frame_search, selec_option, option[0], *option, style='success')
        self.filt_turno.grid(row=1, column=2, padx=5, ipady=4)
        
        self.widget_treeview()
    
    def widget_treeview(self):
        cb = ttk.Treeview(self.table_frame, column=('nombre', 'apellido', 'curso', 'turno'), 
                          style='info', show='headings')

        cb.heading('nombre', text='Nombre', anchor=W)
        cb.heading('apellido', text='Apellido', anchor=W)
        cb.heading('curso', text='Curso', anchor=W)
        cb.heading('turno', text='Turno', anchor=W)
        
        datos = [
            ('Luis Rafael', 'Eyoma', '2º Bach', 'Mañana'),
            ('Manuela ', 'Eyang', '3º Eso', 'Tarde'),
            ('Francisco Javier', 'Nsue', '1º Bach', 'Mañana'),
        ]
        
        for fila in datos:
            cb.insert('', 'end', values=fila)
        
        cb.pack(expand=True, fill=BOTH)
