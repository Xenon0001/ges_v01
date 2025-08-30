import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from .registro_profesores import RegistroProfesores
from .lista_profesores import ListaProfesores
from .perfil_profesores import PerfilProfesor
from .ges_asignaturas import GestionAsignaturas


# Clase principal de la sección de profesores
class Profesores(ttk.Frame):
    """
    Clase principal que gestiona la interfaz de la sección de profesores.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=True)
        self.secciones = {}
        self.inicializar_ui()
        self.mostrar_seccion("Lista") # Inicia en la sección de Listado

    def inicializar_ui(self):
        """Inicializa la interfaz principal con el menú superior y el área de contenido."""
        # Frame superior para los botones de navegación
        menu_frame = ttk.Frame(self, height=200)
        menu_frame.pack(side=TOP, fill=X)

        # Botones del menú
        ttk.Button(menu_frame, text="Gestión de Asignaturas", command=lambda: self.mostrar_seccion("Gestion"), bootstyle=SUCCESS).pack(side=RIGHT, padx=5, pady=5)
        ttk.Button(menu_frame, text="Perfil", command=lambda: self.mostrar_seccion("Perfil"), bootstyle=SUCCESS).pack(side=RIGHT, padx=5, pady=5)
        ttk.Button(menu_frame, text="Registro", command=lambda: self.mostrar_seccion("Registro"), bootstyle=SUCCESS).pack(side=RIGHT, padx=5, pady=5)
        ttk.Button(menu_frame, text="Listado", command=lambda: self.mostrar_seccion("Lista"), bootstyle=SUCCESS).pack(side=RIGHT, padx=5, pady=5)

        # Frame para el contenido de las secciones
        self.contenido_frame = ttk.Frame(self)
        self.contenido_frame.pack(side=BOTTOM, fill=BOTH, expand=True, padx=10, pady=10)

        self.secciones["Registro"] = RegistroProfesores(self.contenido_frame)
        self.secciones["Lista"] = ListaProfesores(self.contenido_frame)
        self.secciones["Perfil"] = PerfilProfesor(self.contenido_frame)
        self.secciones["Gestion"] = GestionAsignaturas(self.contenido_frame)

    def mostrar_seccion(self, nombre_seccion):
        """Oculta todas las secciones y muestra la sección solicitada."""
        try:
            for seccion in self.secciones.values():
                seccion.pack_forget()
            
            seccion_a_mostrar = self.secciones.get(nombre_seccion)
            if seccion_a_mostrar:
                seccion_a_mostrar.pack(fill=BOTH, expand=True)
            else:
                raise ValueError(f"La sección '{nombre_seccion}' no existe.")
        except Exception as e:
            Messagebox.show_error("Error de Navegación", f"No se pudo mostrar la sección. Error: {e}")

# ---
# Ejemplo de uso: Ejecutar la aplicación
# ---
# if __name__ == "__main__":
#     root = ttk.Window(themename="superhero") # Utiliza un tema de ttkbootstrap
#     root.title("Sistema de Gestión Escolar - Profesores")
#     root.geometry("800x600")

#     profesores_app = Profesores(root)
#     root.mainloop()