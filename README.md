|-------------------------------------------------------------------------------------------------------|
|                                                                                                       |
|                                  | |    |  \  /  |                                                    |
|                                  | |    |   \/   |                                                    |
|                                  | |    | |\__/| |                                                    |
|                                  | |    | |    | | g                                                  |
|                                                                                                       |
|                                                                                                       |
|                                                                                                       |
|-------------------------------------------------------------------------------------------------------|

# GES — Sistema de Gestión Escolar

Sistema de gestión escolar diseñado para centros educativos en Guinea Ecuatorial. Desarrollado con Python, SQLite y Tkinter, funciona completamente offline y en redes locales sin necesidad de conexión a internet.

---

## Características principales

- **Gestión de estudiantes** — registro, número de matrícula automático, asignación a aulas
- **Gestión académica** — materias, aulas, importación de notas desde Excel, alertas de rendimiento
- **Gestión financiera** — seguimiento de pagos, morosidad, calendarios de pago por tutor
- **Calendarios de pago** — agrupación de varios hijos por tutor con cuotas personalizadas y pago inicial
- **Reportes PDF** — boletines académicos, morosidad, rendimiento por aula
- **Configuración del centro** — estructura académica (niveles, grados, aulas), precios de matrícula por nivel, gestión de usuarios
- **Modo servidor/cliente** — uso en red local (LAN) desde múltiples equipos
- **Moneda local** — Franco CFA (FCFA)

---

## Tecnologías

| Componente        | Tecnología              |
|-------------------|-------------------------|
| Lenguaje          | Python 3.11+            |
| Interfaz          | Tkinter / CustomTkinter |
| Base de datos     | SQLite                  |
| API (modo LAN)    | FastAPI + Uvicorn       |
| Reportes PDF      | ReportLab               |
| Importación Excel | openpyxl                |

---

## Requisitos

- Python 3.11 o superior
- Windows 10/11 (versión de escritorio)
- Sin conexión a internet requerida

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Xenon0001/ges.git
cd ges

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

Al ejecutar por primera vez, GES crea automáticamente la base de datos con el usuario administrador por defecto:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

> Se recomienda cambiar la contraseña desde Configuración → Usuarios tras el primer inicio de sesión.

---

## Modos de uso

### Modo normal (un solo equipo)

```bash
python main.py
```

### Modo servidor (red local)

```bash
python api/server.py
```

El servidor queda disponible en `http://0.0.0.0:8000`. Los demás equipos de la red se conectan desde Configuración → Modo cliente introduciendo la IP del servidor.

Documentación de la API disponible en `http://localhost:8000/docs`.

---

## Estructura del proyecto

```
ges/
├── main.py                  # Punto de entrada
├── config.py                # Constantes y configuración
├── config.json              # Configuración del centro
├── data/
│   └── ges.db               # Base de datos SQLite
├── core/
│   └── engine.py            # Lógica de negocio
├── database/
│   ├── models.py            # Definición de tablas
│   ├── repository.py        # Capa de acceso a datos
│   └── connection.py        # Conexión a SQLite
├── services/                # Servicios por módulo
├── api/                     # Servidor FastAPI (modo LAN)
├── ui/                      # Vistas de la interfaz
└── utils/                   # Utilidades (importador Excel, etc.)
```

---

## Roles de usuario

| Rol        | Acceso                                               |
|------------|------------------------------------------------------|
| Directiva  | Acceso completo, gestión de usuarios y configuración |
| Secretaria | Gestión de estudiantes, académico y finanzas         |
| Usuario    | Solo lectura                                         |

---

## Flujo básico de uso

1. **Configurar el centro** — Configuración → Centro (nombre, año académico, precios de matrícula por nivel)
2. **Crear la estructura académica** — Configuración → Estructura (niveles, grados, aulas)
3. **Registrar estudiantes** — Estudiantes → Nuevo Estudiante
4. **Asignar calendarios de pago** — Al registrar un estudiante el sistema detecta si el tutor ya tiene calendario; si no, ofrece crearlo
5. **Importar notas** — Académico → Importar (descargar plantilla Excel, rellenar y subir)
6. **Generar reportes** — Reportes → seleccionar tipo y generar PDF

---

## Autor

Desarrollado por **Luis Rafael Eyoma** — [Xenon.py](https://luisrafael.netlify.app)  
Bata, Guinea Ecuatorial

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.