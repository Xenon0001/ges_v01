# 🧱 C) ESTRUCTURA DEFINITIVA DEL PROYECTO — GES

Principio:

> Separar claramente:
> Interfaz · Lógica · Acceso a datos · Red

Y que el núcleo funcione igual en modo Normal o Servidor.

---

# 📂 Estructura Raíz

```
ges/
│
├── main.py
├── config.py
├── config.json
│
├── core/
├── database/
├── services/
├── api/
├── ui/
├── utils/
│
└── assets/
```

Simple. Sin 40 carpetas.

---

# 🔹 main.py

Punto de entrada.

Responsable de:

* Leer config.json
* Determinar modo (normal / server / client)
* Iniciar:

  * UI standalone
  * Servidor FastAPI
  * Cliente conectado

Nada más.

---

# 🔹 config.py

Contiene:

* Constantes
* Puerto por defecto
* Rutas
* Configuración global

---

# 🔹 core/

Aquí vive el corazón lógico del sistema.

```
core/
├── auth.py
├── permissions.py
├── session.py
├── engine.py
```

engine.py:
Contiene la lógica principal del negocio.

Ejemplo:

* calcular_promedios()
* detectar_alertas()
* calcular_morosidad()

⚠ Aquí no hay SQLite ni FastAPI.
Solo lógica pura.

---

# 🔹 database/

Solo acceso a datos.

```
database/
├── connection.py
├── models.py
├── repository.py
```

connection.py:

* Conecta SQLite

repository.py:

* Funciones CRUD
* Consultas

Nada de lógica de negocio aquí.

---

# 🔹 services/

Orquestación entre lógica y base de datos.

```
services/
├── student_service.py
├── academic_service.py
├── finance_service.py
├── report_service.py
```

Aquí se combinan:

* repository
* engine

Pero no UI.

---

# 🔹 api/ (Solo modo servidor)

```
api/
├── server.py
├── routes_students.py
├── routes_academic.py
├── routes_finance.py
├── routes_auth.py
```

Aquí viven:

* Endpoints FastAPI
* Validación de requests
* Control de permisos

Nada de lógica profunda aquí.

Solo llamadas a services.

---

# 🔹 ui/

Interfaz (Tkinter / CustomTkinter)

```
ui/
├── app.py
├── login.py
├── dashboard.py
├── academic_view.py
├── students_view.py
├── finance_view.py
├── reports_view.py
├── settings_view.py
```

Cada archivo = una ventana principal.

La UI solo llama a:

* services (modo normal)
* API (modo cliente)

Nunca accede directamente a SQLite.

---

# 🔹 utils/

```
utils/
├── excel_importer.py
├── pdf_generator.py
├── helpers.py
```

Herramientas auxiliares.

---

# 🔹 assets/

* Iconos
* Logos
* Recursos visuales

---

# 🎯 Lo más importante de toda esta arquitectura

El núcleo (core + services + database) es compartido.

Modo Normal:
UI → Services → Repository → SQLite

Modo Cliente:
UI → HTTP → API → Services → Repository → SQLite

La lógica no cambia.

Solo cambia el transporte.

Eso hace el proyecto sostenible.

---

# 🔒 Reglas internas obligatorias

1. UI nunca toca SQLite.
2. API nunca contiene lógica de negocio.
3. Services no contienen código visual.
4. Core no sabe que existe FastAPI.
5. Nada depende directamente de Tkinter fuera de ui/.

Si respetas esto,
no volverás a tener “código basura”.

---

# 📊 Número real de ventanas del MVP

Login
Selector modo (solo primera vez)
Dashboard
Académico
Estudiantes
Finanzas
Reportes
Configuración

Total: 8 principales.

Subventanas modales para formularios.

Controlado. No infinito.
