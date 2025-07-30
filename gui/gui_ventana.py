import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.gui_menu import SideBar
from gui.gui_contenido_dinamico import MainFrame

from gui.gui_student.gui_estudiantes import EstudiantesSeccion
from gui.gui_control_panel.gui_panel import Panel


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera", title="GES - Gestor Educativo Simple")
        self.geometry("1100x700")
        self.minsize(1000, 600)
        
        
        self.main_frame = MainFrame(self)
        self.menu = SideBar(self, self.mostrar_seccion)
        
        self.menu.pack(side=LEFT, fill=Y)
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.frames = {
            "inicio": self.mostrar_inicio,
            "estudiantes": lambda: self.main_frame.cambiar_contenido(EstudiantesSeccion)
        }
        
        self.mostrar_inicio()
    
    def mostrar_inicio(self):
        self.main_frame.limpiar()
        self.panel = Panel(self.main_frame)
        self.panel.pack(fill=BOTH, expand=True)
    
    def mostrar_seccion(self, nombre):
        if nombre in self.frames:
            self.frames[nombre]()