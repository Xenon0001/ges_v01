import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

class RegistrarEstudiantes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pack(fill='both', expand=True, padx=15, pady=15)
        self.columnconfigure(0, weight=3) # Formulario ocupa más espacio
        self.columnconfigure(1, weight=1) # Cards de cursos ocupan menos
        self.rowconfigure(0, weight=1)

        # Contenedor principal para el formulario y los cards
        main_frame = ttk.Frame(self, padding="15")
        main_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Crear el contenedor del formulario a la izquierda
        self.form_frame = ttk.LabelFrame(main_frame, text="Datos del Estudiante y Tutor", padding="15")
        self.form_frame.grid(row=0, column=0, padx=(0, 15), sticky='nsew')
        self.form_frame.columnconfigure(1, weight=1)
        self.setup_form()

        # Crear el contenedor de los cards a la derecha
        self.cards_frame = ttk.LabelFrame(main_frame, text="Estadísticas de Cursos", padding="15")
        self.cards_frame.grid(row=0, column=1, padx=(15, 0), sticky='nsew')
        self.setup_cards()
        
    def setup_form(self):
        """Configura el formulario de registro."""
        # Título
        ttk.Label(self.form_frame, text="Registrar Estudiante", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Campos del formulario con btk.Label y btk.Entry
        labels = ["Nombre:", "Apellido:", "Curso:", "Clase:", "Centro de procedencia:", "Fecha de nacimiento:", "Nombre del tutor:", "Número telefónico:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(self.form_frame, text=label_text).grid(row=i+1, column=0, padx=5, pady=5, sticky='w')
            if label_text == "Clase:":
                self.clase_combo = ttk.Combobox(self.form_frame, values=[chr(ord('A') + i) for i in range(14)], state="readonly")
                self.clase_combo.grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
                self.entries[label_text] = self.clase_combo
            elif label_text == "Fecha de nacimiento:":
                self.fecha_nac_entry = ttk.DateEntry(self.form_frame, bootstyle="info")
                self.fecha_nac_entry.grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
                self.entries[label_text] = self.fecha_nac_entry
            else:
                entry = ttk.Entry(self.form_frame, bootstyle="info")
                entry.grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
                self.entries[label_text] = entry

        # Checkbox para el "calendario"
        self.calendario_var = tk.BooleanVar()
        self.calendario_check = ttk.Checkbutton(
            self.form_frame,
            text="Aplicar Calendario de Pagos",
            variable=self.calendario_var,
            bootstyle="round-toggle"
        )
        self.calendario_check.grid(row=len(labels) + 1, column=0, columnspan=2, padx=5, pady=15, sticky='w')

        # Botón de Agregar
        self.agregar_btn = ttk.Button(self.form_frame, text="Agregar Estudiante", command=self.agregar_estudiante, bootstyle="success")
        self.agregar_btn.grid(row=len(labels) + 2, column=0, columnspan=2, pady=10)

    def setup_cards(self):
        """Configura la visualización de datos estáticos (cards)."""
        cursos_data = {
            "1º ESO": "22/32",
            "2º ESO": "25/35",
            "3º ESO": "18/30",
            "4º ESO": "20/28"
        }

        for curso, data in cursos_data.items():
            self.create_card(self.cards_frame, curso, data)
            
    def create_card(self, parent, title, value):
        """Crea una card con estilo minimalista."""
        card = ttk.Frame(parent, bootstyle="secondary", padding="15")
        card.pack(fill='x', padx=5, pady=5)

        ttk.Label(card, text=title, font=("Helvetica", 12, "bold"), bootstyle="inverse-secondary").pack(pady=(0, 5))
        ttk.Label(card, text=f"Alumnos: {value}", font=("Helvetica", 16), bootstyle="inverse-secondary").pack()

    def validar_campos(self):
        """Valida que los campos de entrada obligatorios no estén vacíos."""
        required_fields = ["Nombre:", "Apellido:", "Curso:", "Clase:", "Centro de procedencia:", "Fecha de nacimiento:", "Nombre del tutor:", "Número telefónico:"]
        for field in required_fields:
            if field == "Clase:":
                value = self.clase_combo.get()
            elif field == "Fecha de nacimiento:":
                value = self.fecha_nac_entry.entry.get()
            else:
                value = self.entries[field].get()
            
            if not value:
                raise ValueError(f"El campo '{field}' no puede estar vacío.")

    def agregar_estudiante(self):
        """Maneja la lógica del botón Agregar."""
        try:
            self.validar_campos()
            
            # Mostrar el Toplevel adecuado
            if self.calendario_var:
                self.show_calendario_toplevel()
            else:
                self.show_pago_toplevel()
                
        except ValueError as e:
            Messagebox.show_error(title="Error de Validación", message=str(e))
        except Exception as e:
            Messagebox.show_error(title="Error", message=f"Ha ocurrido un error inesperado: {e}")

    def show_calendario_toplevel(self):
        """Muestra el toplevel para el caso de calendario activado."""
        toplevel = tk.Toplevel(self)
        toplevel.title("Configurar Calendario de Pagos")
        toplevel.resizable=(False, False)
        toplevel.geometry("350x250")

        frame = ttk.Frame(toplevel, padding="20")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Nombre del Calendario:", font=('Helvetica', 10, 'bold')).pack(pady=(0, 5))
        self.nombre_calendario_entry = ttk.Entry(frame, bootstyle="info")
        self.nombre_calendario_entry.pack(fill='x', padx=5, pady=(0, 10))

        ttk.Label(frame, text="Pago Inicial:", font=('Helvetica', 10, 'bold')).pack(pady=(0, 5))
        self.pago_inicial_entry = ttk.Entry(frame, bootstyle="info")
        self.pago_inicial_entry.pack(fill='x', padx=5, pady=(0, 10))
        
        ttk.Button(frame, text="Guardar", command=lambda: self.guardar_pago(toplevel, True), bootstyle="success").pack(pady=(15, 0))
        
    def show_pago_toplevel(self):
        """Muestra el toplevel para el caso de calendario desactivado."""
        toplevel = tk.Toplevel(self)
        toplevel.title=("Configurar Pago Inicial")
        toplevel.resizable=(False, False)
        toplevel.geometry("350x200")
        toplevel.grab_set()

        frame = ttk.Frame(toplevel, padding="20")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Pago Inicial:", font=('Helvetica', 10, 'bold')).pack(pady=(0, 5))
        self.pago_inicial_entry = ttk.Entry(frame, bootstyle="info")
        self.pago_inicial_entry.pack(fill='x', padx=5, pady=(0, 10))

        ttk.Button(frame, text="Guardar", command=lambda: self.guardar_pago(toplevel, False), bootstyle="success").pack(pady=(15, 0))

    def guardar_pago(self, toplevel, es_calendario):
        """Maneja la lógica del botón de guardar en los toplevels."""
        try:
            pago_inicial = float(self.pago_inicial_entry.get())
            
            if es_calendario:
                nombre_calendario = self.nombre_calendario_entry.get()
                if not nombre_calendario:
                    raise ValueError("El nombre del calendario no puede estar vacío.")
                print(f"Pago inicial y calendario guardados: {pago_inicial}, {nombre_calendario}")
            else:
                print(f"Pago inicial guardado: {pago_inicial}")
                
            toplevel.destroy()
            Messagebox.show_info(title="Éxito", message="Estudiante registrado correctamente.")

        except ValueError as e:
            Messagebox.show_error(title="Error de Entrada", message=f"Error: {e}. Por favor, ingresa un número válido para el pago.")
        except Exception as e:
            Messagebox.show_error(title="Error", message=f"Ha ocurrido un error al guardar el pago: {e}")