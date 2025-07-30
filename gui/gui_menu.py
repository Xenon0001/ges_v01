import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *



class SideBar(ttk.Frame):
    def __init__(self, parent, callback, **kwargs):
        super().__init__(bootstyle="secondary", padding=10, **kwargs)
        
        self.callback = callback
        
        self.crear_botones()
    
    def crear_botones(self):
        botones = {
            "inicio" : "Inicio",
            "estudiantes" : "Estudiantes",
            "profesores" : "Profesores",
            "boletin" : "Boletín",
            "ampa" : "AMPA",
            "ajustes" : "Ajustes"
        }
        
        
        for id, texto in botones.items():
            btn = ttk.Button(self, text=texto, bootstyle=("light", "link"), command=lambda f=id: self.callback(f), width=20)
            
            if id == "ajustes":
                btn.pack(side=BOTTOM, fill=X, pady=(0, 35))
            else:
                btn.pack(fill=X, pady=5)