# GES - Gestor Educativo Simple (ges_v01)

GES es una aplicación de escritorio diseñada para facilitar la gestión educativa. Permite a los usuarios administrar estudiantes, visualizar paneles de control y navegar entre diferentes secciones de manera intuitiva.

## Características

- **Panel de Control**: Una vista inicial con información general y accesos rápidos.
- **Gestión de Estudiantes**: Permite agregar, editar y visualizar información de los estudiantes.
- **Interfaz Dinámica**: Contenedor principal que cambia dinámicamente según la sección seleccionada.
- **Diseño Moderno**: Utiliza `ttkbootstrap` para un diseño atractivo y moderno.

## Estructura del Proyecto

```plaintext
ges_v01/
├── [app.py](http://_vscodecontentref_/1)                        # Punto de entrada principal de la aplicación
├── gui/
│   ├── __init__.py               # Archivo de inicialización del módulo GUI
│   ├── gui_ventana.py            # Configuración de la ventana principal
│   ├── gui_menu.py               # Menú lateral de navegación
│   ├── gui_contenido_dinamico.py # Contenedor dinámico para las secciones
│   ├── gui_control_panel/
│   │   ├── __init__.py
│   │   ├── gui_panel.py          # Panel de control (sección "Inicio")
│   ├── gui_student/
│       ├── __init__.py
│       ├── gui_estudiantes.py    # Gestión de estudiantes
├── model/
│   ├── __init__.py               # Archivo de inicialización del módulo de modelos
├── .gitignore                    # Archivos y carpetas ignorados por Git
├── [README.md](http://_vscodecontentref_/2)                     # Documentación del proyecto
```
### Requisitos

Python 3.10 o superior
Paquetes necesarios (instalarlos con pip):
ttkbootstrap

### Instalación

Clona este repositorio:

```
git clone https://github.com/Xenon0001/ges_v01.git
cd ges_v01
```
Instala las dependencias:

```
pip install ttkbootstrap
```
Ejecuta la aplicación:

```
python app.py
```

### Licencia.
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

### Autor
- **Xenon0001**