"""
Vista para gestión de estructura académica: niveles, grados y aulas
Integrada como pestaña en el módulo de Configuración
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional
from database.repository import level_repo, grade_repo, classroom_repo


class AcademicStructureView:
    """Vista principal para gestión de estructura académica"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        self.main_frame = ttk.Frame(self.parent_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(self.main_frame, text="Estructura Académica", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas
        self.create_levels_tab()
        self.create_grades_tab()
        self.create_classrooms_tab()
    
    def create_levels_tab(self):
        """Crea pestaña de Niveles"""
        self.levels_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.levels_frame, text="Niveles")
        
        # Frame superior con botón crear
        levels_top = ttk.Frame(self.levels_frame)
        levels_top.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(levels_top, text="+ Crear Nivel", 
                  command=self.create_level).pack(side=tk.RIGHT)
        
        # Tabla de niveles
        self.create_levels_table()
    
    def create_levels_table(self):
        """Crea tabla para mostrar niveles"""
        # Frame para tabla
        table_frame = ttk.Frame(self.levels_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ("id", "name")
        self.levels_tree = ttk.Treeview(table_frame, columns=columns, 
                                        show="headings", height=15)
        
        self.levels_tree.heading("id", text="ID")
        self.levels_tree.heading("name", text="Nombre")
        
        self.levels_tree.column("id", width=50, anchor=tk.CENTER)
        self.levels_tree.column("name", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.levels_tree.yview)
        self.levels_tree.configure(yscrollcommand=scrollbar.set)
        
        self.levels_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón de editar
        self.levels_tree.bind("<Double-Button-1>", lambda e: self.edit_level())
    
    def create_grades_tab(self):
        """Crea pestaña de Grados"""
        self.grades_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.grades_frame, text="Grados")
        
        # Frame superior con selector y botón
        grades_top = ttk.Frame(self.grades_frame)
        grades_top.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(grades_top, text="Nivel:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.level_var = tk.StringVar()
        self.level_combo = ttk.Combobox(grades_top, textvariable=self.level_var, 
                                        state="readonly", width=20)
        self.level_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.level_combo.bind("<<ComboboxSelected>>", self.on_level_selected)
        
        self.create_grade_btn = ttk.Button(grades_top, text="+ Crear Grado", 
                                          command=self.create_grade, state=tk.DISABLED)
        self.create_grade_btn.pack(side=tk.RIGHT)
        
        # Tabla de grados
        self.create_grades_table()
    
    def create_grades_table(self):
        """Crea tabla para mostrar grados"""
        # Frame para tabla
        table_frame = ttk.Frame(self.grades_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ("id", "name", "level_name")
        self.grades_tree = ttk.Treeview(table_frame, columns=columns, 
                                        show="headings", height=15)
        
        self.grades_tree.heading("id", text="ID")
        self.grades_tree.heading("name", text="Nombre")
        self.grades_tree.heading("level_name", text="Nivel")
        
        self.grades_tree.column("id", width=50, anchor=tk.CENTER)
        self.grades_tree.column("name", width=150)
        self.grades_tree.column("level_name", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=scrollbar.set)
        
        self.grades_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón de editar
        self.grades_tree.bind("<Double-Button-1>", lambda e: self.edit_grade())
    
    def create_classrooms_tab(self):
        """Crea pestaña de Aulas"""
        self.classrooms_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.classrooms_frame, text="Aulas")
        
        # Frame superior con selectores y botón
        classrooms_top = ttk.Frame(self.classrooms_frame)
        classrooms_top.pack(fill=tk.X, pady=(0, 10))
        
        # Primera fila - Nivel
        ttk.Label(classrooms_top, text="Nivel:").grid(row=0, column=0, padx=(0, 5), pady=2, sticky='w')
        self.level_aulas_var = tk.StringVar()
        self.level_aulas_combo = ttk.Combobox(classrooms_top, textvariable=self.level_aulas_var, 
                                              state="readonly", width=20)
        self.level_aulas_combo.grid(row=0, column=1, padx=(0, 10), pady=2)
        self.level_aulas_combo.bind("<<ComboboxSelected>>", self.on_level_aulas_selected)
        
        # Segunda fila - Grado
        ttk.Label(classrooms_top, text="Grado:").grid(row=1, column=0, padx=(0, 5), pady=2, sticky='w')
        self.grade_aulas_var = tk.StringVar()
        self.grade_aulas_combo = ttk.Combobox(classrooms_top, textvariable=self.grade_aulas_var, 
                                               state="readonly", width=25)
        self.grade_aulas_combo.grid(row=1, column=1, padx=(0, 10), pady=2)
        self.grade_aulas_combo.bind("<<ComboboxSelected>>", self.on_grade_aulas_selected)
        
        # Botón crear
        self.create_classroom_btn = ttk.Button(classrooms_top, text="+ Crear Aula", 
                                              command=self.create_classroom, state=tk.DISABLED)
        self.create_classroom_btn.grid(row=1, column=2, padx=(10, 0), pady=2)
        
        # Tabla de aulas
        self.create_classrooms_table()
    
    def create_classrooms_table(self):
        """Crea tabla para mostrar aulas"""
        # Frame para tabla
        table_frame = ttk.Frame(self.classrooms_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ("id", "name", "grade_name", "shift")
        self.classrooms_tree = ttk.Treeview(table_frame, columns=columns, 
                                            show="headings", height=15)
        
        self.classrooms_tree.heading("id", text="ID")
        self.classrooms_tree.heading("name", text="Nombre")
        self.classrooms_tree.heading("grade_name", text="Grado")
        self.classrooms_tree.heading("shift", text="Turno")
        
        self.classrooms_tree.column("id", width=50, anchor=tk.CENTER)
        self.classrooms_tree.column("name", width=100)
        self.classrooms_tree.column("grade_name", width=150)
        self.classrooms_tree.column("shift", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.classrooms_tree.yview)
        self.classrooms_tree.configure(yscrollcommand=scrollbar.set)
        
        self.classrooms_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón de editar
        self.classrooms_tree.bind("<Double-Button-1>", lambda e: self.edit_classroom())
    
    def load_data(self):
        """Carga datos iniciales"""
        self.load_levels()
        self.load_grades()
        self.load_classrooms()
        
        # Inicializar combos de Aulas
        levels = level_repo.get_all()
        level_names = [level['name'] for level in levels]
        self.level_aulas_combo['values'] = level_names
    
    def load_levels(self):
        """Carga niveles en combo y tabla"""
        # Limpiar tabla
        for item in self.levels_tree.get_children():
            self.levels_tree.delete(item)
        
        # Cargar datos
        levels = level_repo.get_all()
        
        # Actualizar combo de grados
        level_names = [level['name'] for level in levels]
        self.level_combo['values'] = level_names
        
        # Llenar tabla
        for level in levels:
            self.levels_tree.insert("", tk.END, values=(
                level['id'], level['name']
            ))
    
    def load_grades(self):
        """Carga grados según nivel seleccionado"""
        # Limpiar tabla
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        if not self.level_var.get():
            return
        
        # Obtener nivel seleccionado
        levels = level_repo.get_all()
        selected_level = None
        for level in levels:
            if level['name'] == self.level_var.get():
                selected_level = level
                break
        
        if not selected_level:
            return
        
        # Cargar grados del nivel
        grades = grade_repo.get_by_level(selected_level['id'])
        
        # Llenar tabla
        for grade in grades:
            self.grades_tree.insert("", tk.END, values=(
                grade['id'], grade['name'], selected_level['name']
            ))
    
    def load_classrooms(self):
        """Carga aulas según grado seleccionado"""
        # Limpiar tabla
        for item in self.classrooms_tree.get_children():
            self.classrooms_tree.delete(item)
        
        if not self.grade_aulas_var.get():  # Usar grade_aulas_var
            return
        
        # Obtener grado seleccionado
        grades = grade_repo.get_all()
        selected_grade = None
        for grade in grades:
            grade_name = f"{grade['name']}"
            if grade_name == self.grade_aulas_var.get():  # Usar grade_aulas_var
                selected_grade = grade
                break
        
        if not selected_grade:
            return
        
        # Cargar aulas del grado
        classrooms = classroom_repo.find_by('grade_id', selected_grade['id'])
        
        # Llenar tabla
        for classroom in classrooms:
            self.classrooms_tree.insert("", tk.END, values=(
                classroom['id'], classroom['name'], self.grade_aulas_var.get(),  # Usar grade_aulas_var
                classroom['shift']
            ))
    
    def on_level_selected(self, event=None):
        """Evento al seleccionar nivel"""
        if self.level_var.get():
            self.create_grade_btn.config(state=tk.NORMAL)
            self.load_grades()
            
            # Actualizar combo de grados para aulas
            grades = grade_repo.get_by_level(
                next(l['id'] for l in level_repo.get_all() 
                     if l['name'] == self.level_var.get())
            )
            grade_names = [grade['name'] for grade in grades]
            self.grade_aulas_combo['values'] = grade_names
            self.grade_aulas_combo.set('')
            self.create_classroom_btn.config(state=tk.DISABLED)
        else:
            self.create_grade_btn.config(state=tk.DISABLED)
    
    def on_grade_selected(self, event=None):
        """Evento al seleccionar grado"""
        if self.grade_var.get():
            self.create_classroom_btn.config(state=tk.NORMAL)
            self.load_classrooms()
        else:
            self.create_classroom_btn.config(state=tk.DISABLED)
    
    def create_level(self):
        """Abre diálogo para crear nivel"""
        dialog = LevelDialog(self.parent_frame, "Crear Nivel")
        if dialog.result:
            try:
                level_repo.create({'name': dialog.result})
                self.load_levels()
                messagebox.showinfo("Éxito", "Nivel creado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear nivel: {str(e)}")
    
    def edit_level(self):
        """Abre diálogo para editar nivel"""
        selection = self.levels_tree.selection()
        if not selection:
            return
        
        item = self.levels_tree.item(selection[0])
        level_id = item['values'][0]
        level_name = item['values'][1]
        
        dialog = LevelDialog(self.parent_frame, "Editar Nivel", level_name)
        if dialog.result and dialog.result != level_name:
            try:
                level_repo.update(level_id, {'name': dialog.result})
                self.load_levels()
                messagebox.showinfo("Éxito", "Nivel actualizado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar nivel: {str(e)}")
    
    def create_grade(self):
        """Abre diálogo para crear grado"""
        if not self.level_var.get():
            messagebox.showwarning("Advertencia", "Seleccione un nivel primero")
            return
        
        dialog = GradeDialog(self.parent_frame, "Crear Grado", self.level_var.get())
        if dialog.result:
            try:
                # Obtener ID del nivel
                level_id = next(l['id'] for l in level_repo.get_all() 
                               if l['name'] == self.level_var.get())
                
                grade_repo.create({
                    'level_id': level_id,
                    'name': dialog.result
                })
                self.load_grades()
                self.on_level_selected()  # Actualiza grade_combo de Aulas
                messagebox.showinfo("Éxito", "Grado creado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear grado: {str(e)}")
    
    def edit_grade(self):
        """Abre diálogo para editar grado"""
        selection = self.grades_tree.selection()
        if not selection:
            return
        
        item = self.grades_tree.item(selection[0])
        grade_id = item['values'][0]
        grade_name = item['values'][1]
        level_name = item['values'][2]
        
        dialog = GradeDialog(self.parent_frame, "Editar Grado", level_name, grade_name)
        if dialog.result and dialog.result != grade_name:
            try:
                grade_repo.update(grade_id, {'name': dialog.result})
                self.load_grades()
                messagebox.showinfo("Éxito", "Grado actualizado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar grado: {str(e)}")
    
    def create_classroom(self):
        """Abre diálogo para crear aula"""
        if not self.grade_aulas_var.get():  # Usar grade_aulas_var
            messagebox.showwarning("Advertencia", "Seleccione un grado primero")
            return
        
        dialog = ClassroomDialog(self.parent_frame, "Crear Aula", self.grade_aulas_var.get())
        if dialog.result:
            try:
                # Obtener ID del grado
                grades = grade_repo.get_all()
                grade_id = None
                for grade in grades:
                    level_id = next(l['id'] for l in level_repo.get_all() 
                                  if l['name'] == self.level_aulas_var.get())  # Usar level_aulas_var
                    if grade['level_id'] == level_id and grade['name'] == self.grade_aulas_var.get():  # Usar grade_aulas_var
                        grade_id = grade['id']
                        break
                
                if grade_id:
                    classroom_repo.create({
                        'grade_id': grade_id,
                        'name': dialog.result['name'],
                        'shift': dialog.result['shift']
                    })
                    self.load_classrooms()
                    messagebox.showinfo("Éxito", "Aula creada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear aula: {str(e)}")
    
    def on_level_aulas_selected(self, event=None):
        """Evento al seleccionar nivel en pestaña Aulas"""
        if self.level_aulas_var.get():
            # Obtener ID del nivel seleccionado
            levels = level_repo.get_all()
            selected_level = None
            for level in levels:
                if level['name'] == self.level_aulas_var.get():
                    selected_level = level
                    break
            
            if selected_level:
                # Actualizar combo de grados
                grades = grade_repo.get_by_level(selected_level['id'])
                grade_names = [grade['name'] for grade in grades]
                self.grade_aulas_combo['values'] = grade_names
                self.grade_aulas_combo.set('')
                self.create_classroom_btn.config(state=tk.DISABLED)
        else:
            self.grade_aulas_combo['values'] = []
            self.grade_aulas_combo.set('')
            self.create_classroom_btn.config(state=tk.DISABLED)
    
    def on_grade_aulas_selected(self, event=None):
        """Evento al seleccionar grado en pestaña Aulas"""
        if self.grade_aulas_var.get():
            self.create_classroom_btn.config(state=tk.NORMAL)
            self.load_classrooms()
        else:
            self.create_classroom_btn.config(state=tk.DISABLED)
    
    def edit_classroom(self):
        """Abre diálogo para editar aula"""
        selection = self.classrooms_tree.selection()
        if not selection:
            return
        
        item = self.classrooms_tree.item(selection[0])
        classroom_id = item['values'][0]
        classroom_name = item['values'][1]
        grade_name = item['values'][2]
        shift = item['values'][3]
        
        dialog = ClassroomDialog(self.parent_frame, "Editar Aula", grade_name, 
                                classroom_name, shift)
        if dialog.result:
            try:
                update_data = {}
                if dialog.result['name'] != classroom_name:
                    update_data['name'] = dialog.result['name']
                if dialog.result['shift'] != shift:
                    update_data['shift'] = dialog.result['shift']
                
                if update_data:
                    classroom_repo.update(classroom_id, update_data)
                    self.load_classrooms()
                    messagebox.showinfo("Éxito", "Aula actualizada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar aula: {str(e)}")


class LevelDialog:
    """Diálogo para crear/editar niveles"""
    
    def __init__(self, parent, title, initial_value=""):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (150 // 2)
        self.dialog.geometry(f"400x150+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo nombre
        ttk.Label(main_frame, text="Nombre:").pack(anchor=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar(value=initial_value)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 20))
        name_entry.focus()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save).pack(side=tk.RIGHT)
        
        # Enter para guardar
        name_entry.bind("<Return>", lambda e: self.save())
        
        # Esperar cierre
        self.dialog.wait_window()
    
    def save(self):
        """Guarda el resultado"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Advertencia", "Ingrese un nombre válido")
            return
        
        self.result = name
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class GradeDialog:
    """Diálogo para crear/editar grados"""
    
    def __init__(self, parent, title, level_name, initial_value=""):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo nivel (solo lectura)
        ttk.Label(main_frame, text="Nivel:").pack(anchor=tk.W, pady=(0, 5))
        level_label = ttk.Label(main_frame, text=level_name, font=("Arial", 10, "bold"))
        level_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Campo nombre
        ttk.Label(main_frame, text="Nombre:").pack(anchor=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar(value=initial_value)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 20))
        name_entry.focus()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save).pack(side=tk.RIGHT)
        
        # Enter para guardar
        name_entry.bind("<Return>", lambda e: self.save())
        
        # Esperar cierre
        self.dialog.wait_window()
    
    def save(self):
        """Guarda el resultado"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Advertencia", "Ingrese un nombre válido")
            return
        
        self.result = name
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class ClassroomDialog:
    """Diálogo para crear/editar aulas"""
    
    def __init__(self, parent, title, grade_name, initial_name="", initial_shift="Mañana"):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"400x250+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo grado (solo lectura)
        ttk.Label(main_frame, text="Grado:").pack(anchor=tk.W, pady=(0, 5))
        grade_label = ttk.Label(main_frame, text=grade_name, font=("Arial", 10, "bold"))
        grade_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Campo nombre
        ttk.Label(main_frame, text="Nombre:").pack(anchor=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar(value=initial_name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 15))
        name_entry.focus()
        
        # Campo turno
        ttk.Label(main_frame, text="Turno:").pack(anchor=tk.W, pady=(0, 5))
        self.shift_var = tk.StringVar(value=initial_shift)
        shift_combo = ttk.Combobox(main_frame, textvariable=self.shift_var, 
                                  values=["Mañana", "Tarde"], state="readonly", width=38)
        shift_combo.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save).pack(side=tk.RIGHT)
        
        # Enter para guardar
        name_entry.bind("<Return>", lambda e: self.save())
        
        # Esperar cierre
        self.dialog.wait_window()
    
    def save(self):
        """Guarda el resultado"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Advertencia", "Ingrese un nombre válido")
            return
        
        self.result = {
            'name': name,
            'shift': self.shift_var.get()
        }
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()
