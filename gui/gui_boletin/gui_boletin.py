import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Boletin(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="Notas de cada trimestre").pack(expand=True, fill=BOTH)