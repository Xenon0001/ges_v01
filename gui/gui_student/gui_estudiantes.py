import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from .lista_est import ListaEstudiantes
from .registrar_est import RegistrarEstudiantes

class EstudiantesSeccion(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Frames para dividir la interfaz
        menu_frame = ttk.Frame(self, height=200)
        menu_frame.pack(fill=X)
    
        # Botones del menu
        self.btn_menu_registro = ttk.Button(menu_frame, text="Registro", width=20, command= lambda t='registro': self.cambiar_de_seccion(t))
        self.btn_menu_registro.pack(side=RIGHT)
        
        self.btn_menu_lista = ttk.Button(menu_frame, text="Inicio", width=20, command= lambda t='inicio': self.cambiar_de_seccion(t))
        self.btn_menu_lista.pack(side=RIGHT, padx=2)
                
        self.seccion_list = ListaEstudiantes(self)
        self.seccion_list.pack()
        self.seccion_regis = RegistrarEstudiantes(self)
        self.seccion_regis.pack()
        
        self.cambiar_de_seccion('inicio')
    
    # Lógica para cambiar de vista: lo moveré a la carpeta model luego
    def cambiar_de_seccion(self, mostrar):
        if mostrar == 'registro':
            self.seccion_list.pack_forget()
        
            if not self.seccion_regis.winfo_ismapped():
                self.seccion_regis.pack(expand=True, fill=BOTH)
            
        elif mostrar == 'inicio':   
            self.seccion_regis.pack_forget()

            if not self.seccion_list.winfo_ismapped():
                self.seccion_list.pack(expand=True, fill=BOTH)