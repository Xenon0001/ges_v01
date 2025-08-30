import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ListaProfesores(ttk.Frame):
    """Vista general de todos los profesores registrados."""
    def __init__(self, parent):
        super().__init__(parent)
        
        frame_search = ttk.Frame(self, height=100)
        frame_search.pack(fill=X)
        frame_search.pack_propagate(False)
        frame_search.grid_propagate(False)
        
        ttk.Label(frame_search, text="Nombre del profesor", justify=LEFT).grid(row=0, column=0, sticky=W, pady=(20, 5))
        
        self.buscador_est = ttk.Entry(frame_search, width=70, justify=LEFT, show="Nombre")
        self.buscador_est.grid(row=1, column=0, sticky=NSEW, columnspan=2, ipady=4)
        
        option = ['Mañana', 'Tarde', 'Ambos']
        
        selec_option = ttk.StringVar(frame_search)
        selec_option.set(option[0])
        
        self.filt_turno = ttk.OptionMenu(frame_search, selec_option, option[0], *option, style='success')
        self.filt_turno.grid(row=1, column=2, padx=5, ipady=4)
        
        self.inicializar_lista()

    def inicializar_lista(self):
        # Datos estáticos de profesores
        profesores_datos = [
            ("Juan Pérez", "Ingeniería de Software", "Cálculo, Física"),
            ("María Gómez", "Inteligencia Artificial", "Programación, Algoritmos"),
            ("Carlos Ruiz", "Ciberseguridad", "Redes, Seguridad Informática"),
            ("Ana López", "Bases de Datos", "SQL, Diseño de Bases de Datos")
        ]
        
        # Treeview para mostrar la lista de profesores
        columnas = ("Nombre", "Especialidad", "Asignaturas")
        tree = ttk.Treeview(self, columns=columnas, show="headings", style='info')
        
        tree.pack(fill=BOTH, expand=True)
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor=W)

        # Insertar datos estáticos
        for profesor in profesores_datos:
            tree.insert("", "end", values=profesor)