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
Requisitos

Python 3.10 o superior
Paquetes necesarios (instalarlos con pip):
ttkbootstrap

Instalación

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
Uso
Al iniciar la aplicación, se mostrará el Panel de Control.
Usa el menú lateral para navegar entre las secciones:
Inicio: Muestra el panel de control.
Estudiantes: Permite gestionar la información de los estudiantes.
Contribuciones
¡Las contribuciones son bienvenidas! Si deseas colaborar, sigue estos pasos:

Haz un fork del repositorio.
Crea una rama para tu funcionalidad o corrección de errores: git checkout -b feature/nueva-funcionalidad.
Realiza tus cambios y haz un commit: git commit -m "Descripción de los cambios".
Sube tus cambios: git push origin feature/nueva-funcionalidad.
Abre un Pull Request.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

Autor
Luis Rodríguez
GitHub

### ¿Qué incluye este README?
1. **Descripción del proyecto**: Explica qué hace la aplicación.
2. **Características**: Lista las funcionalidades principales.
3. **Estructura del proyecto**: Describe cómo están organizados los archivos.
4. **Requisitos**: Especifica las dependencias necesarias.
5. **Instalación**: Instrucciones para ejecutar el proyecto.
6. **Uso**: Guía básica para navegar por la aplicación.
7. **Contribuciones**: Cómo colaborar en el proyecto.
8. **Licencia**: Información sobre la licencia.
9. **Autor**: Información del creador.