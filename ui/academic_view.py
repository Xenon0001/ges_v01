"""
Academic View - Gestión académica completa
Interfaz profesional para análisis y gestión académica
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Optional
from datetime import datetime

from services.academic_service import AcademicService
from database.repository import subject_repo, classroom_repo, student_repo


class AcademicView:
    """Vista de gestión académica"""
    
    def __init__(self, parent: tk.Frame, config: Dict[str, Any], 
                 academic_service=None):
        self.parent = parent
        self.config = config
        self.academic_service = academic_service if academic_service else AcademicService()
        
        # Estado
        self.current_section = "materias"
        self.academic_year = self.config.get('academic_year', 2024)
        
        # Crear UI
        self.create_widgets()
        
        # Cargar sección inicial
        self.show_section("materias")
    
    def create_widgets(self):
        """Crea todos los widgets"""
        # Header
        self.create_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.parent, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Navegación de secciones
        self.create_section_navigation(main_container)
        
        # Contenido dinámico
        self.create_content_area(main_container)
    
    def create_header(self):
        """Crea el header de la vista"""
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="📚 Gestión Académica",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        # Botones de acción
        right_frame = tk.Frame(header_frame, bg='#2c3e50')
        right_frame.pack(side='right', padx=20, pady=15)
        
        # Botón de ayuda
        help_btn = tk.Button(
            right_frame,
            text="❓",
            font=('Segoe UI', 12),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.show_help
        )
        help_btn.pack(side='left', padx=(0, 5))
        
        # Botón de refrescar
        refresh_btn = tk.Button(
            right_frame,
            text="🔄",
            font=('Segoe UI', 12),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.refresh_current_section
        )
        refresh_btn.pack(side='left')
    
    def create_section_navigation(self, parent):
        """Crea la navegación entre secciones"""
        nav_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        nav_frame.pack(fill='x', pady=(0, 10))
        
        # Contenedor de botones
        buttons_container = tk.Frame(nav_frame, bg='white')
        buttons_container.pack(pady=10, padx=20)
        
        # Botones de navegación
        self.nav_buttons = {}
        
        sections = [
            ("📊 Materias", "materias", '#3498db'),
            ("🏫 Aulas", "aulas", '#27ae60'),
            ("👨‍🎓 Estudiantes", "estudiantes", '#e67e22'),
            ("⚠️ Alertas", "alertas", '#e74c3c')
        ]
        
        for text, section_id, color in sections:
            btn = tk.Button(
                buttons_container,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                bg=color if section_id == self.current_section else '#95a5a6',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=lambda s=section_id: self.show_section(s),
                padx=15,
                pady=8
            )
            btn.pack(side='left', padx=5)
            self.nav_buttons[section_id] = btn
    
    def create_content_area(self, parent):
        """Crea el área de contenido dinámico"""
        # Frame scrollable para contenido
        canvas = tk.Canvas(parent, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.content_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        self.content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def show_section(self, section_id: str):
        """Muestra una sección específica"""
        self.current_section = section_id
        
        # Actualizar colores de botones
        self.update_nav_buttons(section_id)
        
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostrar contenido según sección
        if section_id == "materias":
            self.show_materias_section()
        elif section_id == "aulas":
            self.show_aulas_section()
        elif section_id == "estudiantes":
            self.show_estudiantes_section()
        elif section_id == "alertas":
            self.show_alertas_section()
    
    def update_nav_buttons(self, active_section: str):
        """Actualiza los colores de los botones de navegación"""
        colors = {
            "materias": '#3498db',
            "aulas": '#27ae60',
            "estudiantes": '#e67e22',
            "alertas": '#e74c3c'
        }
        
        for section_id, btn in self.nav_buttons.items():
            if section_id == active_section:
                btn.configure(bg=colors[section_id])
            else:
                btn.configure(bg='#95a5a6')
    
    def refresh_current_section(self):
        """Refresca la sección actual"""
        self.show_section(self.current_section)
    
    def show_help(self):
        """Muestra ayuda"""
        help_text = """
        Gestión Académica - Ayuda
        
        📊 Materias: Análisis de rendimiento por materia
        🏫 Aulas: Rendimiento académico por aula
        👨‍🎓 Estudiantes: Gestión de calificaciones individuales
        ⚠️ Alertas: Alertas académicas activas
        
        Use los botones superiores para navegar entre secciones.
        """
        messagebox.showinfo("Ayuda", help_text)
    
    # Métodos placeholder para cada sección (se implementarán luego)
    def show_materias_section(self):
        """Muestra la sección de análisis por materia"""
        placeholder = tk.Label(
            self.content_frame,
            text="📊 Análisis por Materia - En implementación...",
            font=('Segoe UI', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        placeholder.pack(pady=50)
    
    def show_aulas_section(self):
        """Muestra la sección de rendimiento por aula"""
        placeholder = tk.Label(
            self.content_frame,
            text="🏫 Rendimiento por Aula - En implementación...",
            font=('Segoe UI', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        placeholder.pack(pady=50)
    
    def show_estudiantes_section(self):
        """Muestra la sección de calificaciones por estudiante"""
        placeholder = tk.Label(
            self.content_frame,
            text="👨‍🎓 Calificaciones por Estudiante - En implementación...",
            font=('Segoe UI', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        placeholder.pack(pady=50)
    
    def show_alertas_section(self):
        """Muestra la sección de alertas académicas"""
        placeholder = tk.Label(
            self.content_frame,
            text="⚠️ Alertas Académicas - En implementación...",
            font=('Segoe UI', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        placeholder.pack(pady=50)
