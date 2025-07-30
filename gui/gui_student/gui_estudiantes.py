import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class EstudiantesSeccion(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="Estudiantes").pack(expand=True, fill=BOTH)