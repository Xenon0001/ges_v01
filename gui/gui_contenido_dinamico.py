import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# --- Área de contenido principal ---
class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
    
    def limpiar(self):
        for widget in self.winfo_children():
            widget.pack_forget()
        
        self.update_idletasks()
    
    def cambiar_contenido(self, clase):
        self.limpiar()
        vista = clase(self)
        vista.pack(fill=BOTH, expand=True)