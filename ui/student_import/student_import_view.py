import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Any, Dict, List, Optional

from services.student_import_service import StudentImportService


class StudentImportView:
    """Ventana de importación masiva de estudiantes desde Excel."""

    def __init__(self, parent: tk.Widget, config: Dict[str, Any], on_import_complete=None):
        self.parent = parent
        self.config = config
        self.on_import_complete = on_import_complete
        self.service = StudentImportService()
        self.file_path = ''
        self.import_thread: Optional[threading.Thread] = None
        self.window: Optional[tk.Toplevel] = None
        self.event_queue: Optional[queue.Queue] = None
        self.import_in_progress = False
        self.preview_rows: List[Dict[str, Any]] = []
        self.progress_var = tk.IntVar(value=0)
        self.progress_text = tk.StringVar(value='Esperando archivo...')

    def show(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title('Importar Estudiantes')
        self.window.geometry('920x700')
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.protocol('WM_DELETE_WINDOW', self._on_close)

        self._build_ui()

    def _build_ui(self):
        main_frame = tk.Frame(self.window, bg='#f5f7fa')
        main_frame.pack(fill='both', expand=True, padx=12, pady=12)

        header = tk.Label(
            main_frame,
            text='Importar Estudiantes desde Excel',
            font=('Segoe UI', 16, 'bold'),
            bg='#f5f7fa',
            fg='#2c3e50'
        )
        header.pack(anchor='w', pady=(0, 12))

        top_frame = tk.Frame(main_frame, bg='#f5f7fa')
        top_frame.pack(fill='x', pady=(0, 12))

        select_btn = tk.Button(
            top_frame,
            text='Seleccionar archivo',
            font=('Segoe UI', 10, 'bold'),
            bg='#2980b9',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self._choose_file
        )
        select_btn.pack(side='left')

        self.file_label = tk.Label(
            top_frame,
            text='Ningún archivo seleccionado',
            font=('Segoe UI', 10),
            bg='#f5f7fa',
            fg='#34495e'
        )
        self.file_label.pack(side='left', padx=(12, 0))

        validate_btn = tk.Button(
            top_frame,
            text='Validar archivo',
            font=('Segoe UI', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self._validate_file
        )
        validate_btn.pack(side='right')

        content_frame = tk.Frame(main_frame, bg='#ffffff', relief='solid', borderwidth=1)
        content_frame.pack(fill='both', expand=True, pady=(0, 12))

        preview_label = tk.Label(
            content_frame,
            text='Vista previa de las primeras filas',
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        preview_label.pack(anchor='w', padx=12, pady=(12, 6))

        self.preview_tree = ttk.Treeview(
            content_frame,
            columns=('fila', 'nivel', 'nombre', 'apellido', 'curso', 'aula', 'turno', 'tutor', 'ano'),
            show='headings',
            height=12
        )
        for key, title in [
            ('fila', 'Fila'),
            ('nivel', 'Nivel'),
            ('nombre', 'Nombre'),
            ('apellido', 'Apellido'),
            ('curso', 'Curso'),
            ('aula', 'Aula'),
            ('turno', 'Turno'),
            ('tutor', 'Tutor'),
            ('ano', 'Año Escolar')
        ]:
            self.preview_tree.heading(key, text=title)
            self.preview_tree.column(key, width=100, anchor='center')
        self.preview_tree.column('nombre', width=140, anchor='w')
        self.preview_tree.column('apellido', width=140, anchor='w')
        self.preview_tree.pack(fill='both', expand=True, padx=12, pady=(0, 12))

        progress_frame = tk.Frame(main_frame, bg='#f5f7fa')
        progress_frame.pack(fill='x', pady=(0, 10))

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient='horizontal',
            length=780,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.pack(fill='x', side='left', padx=(0, 6), pady=(0, 4))

        progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_text,
            font=('Segoe UI', 10),
            bg='#f5f7fa',
            fg='#34495e'
        )
        progress_label.pack(side='left')

        action_frame = tk.Frame(main_frame, bg='#f5f7fa')
        action_frame.pack(fill='x', pady=(0, 0))

        self.import_btn = tk.Button(
            action_frame,
            text='Importar estudiantes',
            font=('Segoe UI', 11, 'bold'),
            bg='#8e44ad',
            fg='white',
            relief='flat',
            cursor='hand2',
            state='disabled',
            command=self._start_import
        )
        self.import_btn.pack(side='right', padx=(0, 10))

        self.report_text = tk.Text(
            main_frame,
            height=10,
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#2c3e50',
            state='disabled',
            wrap='word'
        )
        self.report_text.pack(fill='both', expand=True, pady=(6, 0), padx=2)

    def _choose_file(self):
        file_path = filedialog.askopenfilename(
            parent=self.window,
            title='Seleccionar archivo Excel',
            filetypes=[('Excel files', '*.xlsx *.xlsm *.xltx *.xltm')]
        )
        if not file_path:
            return
        self.file_path = file_path
        self.file_label.config(text=file_path)
        self.import_btn.config(state='disabled')
        self._clear_preview()
        self._update_progress_text('Archivo seleccionado. Valide antes de importar.')

    def _validate_file(self):
        if not self.file_path:
            messagebox.showwarning('Archivo requerido', 'Seleccione un archivo Excel primero')
            return
        valid, error_msg = self.service.validate_structure(self.file_path)
        if not valid:
            messagebox.showerror('Estructura inválida', error_msg)
            return
        self._load_preview()
        self.import_btn.config(state='normal')
        self._update_progress_text('Estructura válida. Puede iniciar la importación.')

    def _load_preview(self):
        try:
            preview_rows = self.service.preview_rows(self.file_path, max_rows=15)
        except Exception as exc:
            self._clear_preview()
            messagebox.showerror('Error de vista previa', f'No se pudo cargar la vista previa: {exc}')
            self._update_progress_text('Error al generar vista previa.')
            return

        self._clear_preview()
        for row in preview_rows:
            self.preview_tree.insert(
                '',
                'end',
                values=(
                    row.row_number,
                    row.raw_data.get('nivel', ''),
                    row.raw_data.get('nombre', ''),
                    row.raw_data.get('apellido', ''),
                    row.raw_data.get('curso', ''),
                    row.raw_data.get('aula', ''),
                    row.raw_data.get('turno', ''),
                    row.raw_data.get('tutor', ''),
                    row.raw_data.get('año escolar', '')
                )
            )
        if not preview_rows:
            self._update_progress_text('No se encontraron filas para vista previa.')

    def _clear_preview(self):
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)

    def _start_import(self):
        if not self.file_path:
            messagebox.showwarning('Archivo requerido', 'Seleccione un archivo Excel primero')
            return
        self.import_btn.config(state='disabled')
        self.import_in_progress = True
        self.event_queue = queue.Queue()
        self._update_progress_text('Iniciando importación...')
        self.progress_var.set(0)
        self.report_text.config(state='normal')
        self.report_text.delete('1.0', tk.END)
        self.report_text.config(state='disabled')

        self.import_thread = threading.Thread(target=self._run_import, daemon=True)
        self.import_thread.start()
        self._process_queue()

    def _run_import(self):
        try:
            result = self.service.import_from_excel(
                self.file_path,
                progress_callback=self._queue_progress
            )
            self.event_queue.put(('finished', result))
        except Exception as exc:
            self.event_queue.put(('error', str(exc)))

    def _queue_progress(self, processed: int, total: int, row_number: int, message: str,
                        imported_count: int, omitted_count: int, error_count: int):
        self.event_queue.put((
            'progress', processed, total, row_number, message,
            imported_count, omitted_count, error_count
        ))

    def _process_queue(self):
        if not self.window or not self.window.winfo_exists():
            return

        try:
            while True:
                event = self.event_queue.get_nowait()
                if event[0] == 'progress':
                    _, processed, total, row_number, message, imported_count, omitted_count, error_count = event
                    percentage = int(processed / total * 100) if total else 0
                    self._update_progress(percentage, f"{message} - importados: {imported_count}, omitidos: {omitted_count}, errores: {error_count}")
                elif event[0] == 'finished':
                    _, result = event
                    self._on_import_finished(result)
                    return
                elif event[0] == 'error':
                    _, message = event
                    self._on_import_error(message)
                    return
        except queue.Empty:
            pass

        self.window.after(100, self._process_queue)

    def _on_import_error(self, message: str):
        self.import_in_progress = False
        self.import_btn.config(state='normal')
        self._update_progress_text(f'Error de importación: {message}')
        messagebox.showerror('Error de importación', message)

    def _update_progress(self, percentage: int, message: str):
        self.progress_var.set(percentage)
        self._update_progress_text(message)

    def _update_progress_text(self, text: str):
        self.progress_text.set(text)

    def _on_import_finished(self, result):
        self.import_in_progress = False
        self.import_btn.config(state='normal')
        text_lines = [result.get_summary(), '\n']
        if result.omitted_rows:
            text_lines.append('Omitidos:')
            for row in result.omitted_rows[:10]:
                text_lines.append(f"Fila {row.row_number}: {row.first_name} {row.last_name} - {row.notes}")
            if len(result.omitted_rows) > 10:
                text_lines.append(f"... {len(result.omitted_rows) - 10} omitidos adicionales")
            text_lines.append('\n')
        if result.errors:
            text_lines.append('Errores:')
            for error in result.errors[:10]:
                text_lines.append(f"Fila {error.row_number}: {error.error_type} - {error.message}")
            if len(result.errors) > 10:
                text_lines.append(f"... {len(result.errors) - 10} errores adicionales")
        self.report_text.config(state='normal')
        self.report_text.delete('1.0', tk.END)
        self.report_text.insert(tk.END, '\n'.join(text_lines))
        self.report_text.config(state='disabled')

        if self.on_import_complete:
            self.on_import_complete(result)

    def _on_close(self):
        if self.import_in_progress:
            if not messagebox.askyesno(
                'Importación en progreso',
                'La importación sigue en curso. ¿Cerrar de todas formas? Esto detendrá la ventana pero no el proceso en segundo plano.'
            ):
                return
        if self.window:
            self.window.destroy()
