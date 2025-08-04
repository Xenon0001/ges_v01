import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class EstudiantesSeccion(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        
        self.frames_estudiantes()
    
    def frames_estudiantes(self):
        self.top_frame = ttk.Frame(self, height=200)
        self.top_frame.pack(fill=X)
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(fill=BOTH)
        
        ttk.Button(self.top_frame, text="Inicio").pack(side=LEFT)