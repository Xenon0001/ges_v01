# 🎓 GES – Sistema de Gestión Escolar (Offline)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Desktop App](https://img.shields.io/badge/Type-Desktop%20App-green)
![Offline First](https://img.shields.io/badge/Mode-Offline--First-orange)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow)

---

## 📌 Descripción

**GES (Sistema de Gestión Escolar)** es una aplicación de escritorio **offline-first**, desarrollada en Python, diseñada para **centros educativos con conectividad limitada**, especialmente en contextos como Guinea Ecuatorial.

El objetivo de GES es **resolver de forma práctica y robusta** la gestión diaria de:

* Estudiantes
* Matrículas
* Pagos
* Historial académico
* Reportes y estadísticas

Todo funcionando **sin Internet**, con datos persistentes y controlados localmente.

---

## ⚠️ Estado del Proyecto

### 🚧 **ALERTA: PROYECTO EN DESARROLLO ACTIVO**

> ⚠️ **Estado actual:** En desarrollo
>
> El MVP es **funcional y usable**, pero el proyecto:
>
> * Sigue en fase de validación
> * Está siendo sometido a pruebas intensivas
> * Puede recibir cambios estructurales antes de una versión estable (v1.0)

✔️ Apto para pruebas
❌ No recomendado aún para despliegue masivo sin acompañamiento técnico

---

## ✨ Funcionalidades Principales

* 🔐 Autenticación local con roles
* 👨‍🎓 Gestión completa de estudiantes (CRUD)
* 📝 Matrículas con reglas de negocio
* 💰 Registro y control de pagos
* 📊 Gráficas y reportes académicos y financieros
* 🗂️ Historial académico anual en JSON
* 💾 Backups completos del sistema
* 📤 Exportación de datos a Excel
* ⚙️ Configuración persistente del sistema
* 🖥️ Interfaz gráfica con CustomTkinter

---

## 🧱 Arquitectura

GES utiliza una **arquitectura por capas**, diseñada para ser clara, mantenible y escalable:

```
UI → Services → Repositories → Database
```
```
ges_proy/
├── app/                    # Aplicación principal
│   ├── domain/            # Entidades del dominio (puras)
│   ├── repositories/      # Patrón Repository para acceso a datos
│   ├── services/          # Lógica de negocio
│   └── ui/                # Interfaz de usuario
├── config/                # Configuración del sistema
├── controllers/           # Controladores de la aplicación
├── database/              # Gestión de base de datos
│   ├── models/            # Modelos SQLAlchemy
│   │   ├── base.py        # Base común
│   │   ├── school.py      # School, Grade, Course, etc.
│   │   ├── person.py      # Person, User, Student, Tutor
│   │   └── enrollment.py  # Enrollment, Payment
│   ├── connection.py      # Configuración de conexión
│   ├── db.py             # Gestión y operaciones DB
│   └── models.py         # Modelos consolidados
├── domain/               # Entidades del dominio principales
├── repositories/         # Implementación de repositorios
├── services/             # Servicios de negocio
│   ├── auth_service.py   # Autenticación y usuarios
│   ├── grade_service.py  # Gestión de grados y cursos
│   └── student_service.py # Gestión de estudiantes
├── tests/                # Pruebas del sistema
│   └── test_services_flow.py
├── ui/                   # Componentes de interfaz
│   ├── login_window.py   # Ventana de login
│   └── main_window.py    # Ventana principal
├── .ai/                  # Configuración IA
├── .git/                 # Control de versiones
├── .venv/                # Entorno virtual
├── historial/            # Historial de cambios
├── main.py               # Punto de entrada principal
├── check_payments.py     # Utilidad de pagos
├── test_database.py      # Pruebas de base de datos
├── test_navigation.py    # Pruebas de navegación
├── test_navigation_simple.py # Pruebas simples de navegación
├── test_services.py      # Pruebas de servicios
├── test_structure.py     # Pruebas de estructura
├── requirements.txt      # Dependencias del proyecto
├── .gitignore           # Archivos ignorados por Git
└── ges_database.db      # Base de datos SQLite
```

### Capas principales:

* `app/ui/` → Interfaz gráfica (CustomTkinter)
* `app/services/` → Reglas de negocio
* `app/repositories/` → Acceso a datos
* `app/domain/` → Entidades puras
* `database/` → Modelos y SQLite
* `config/` → Configuración persistente
* `backups/` → Copias de seguridad
* `historial/` → Historial académico

📌 **La UI no accede directamente a la base de datos.**

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **UI:** CustomTkinter
* **Base de datos:** SQLite
* **ORM:** SQLAlchemy
* **Gráficas:** Matplotlib
* **Exportación:** Pandas (Excel)
* **Persistencia:** JSON + SQLite
* **Modo:** 100% Offline

---

## ▶️ Ejecución del Proyecto

```bash
python main.py
```

### Credenciales de prueba (MVP):

* Usuario: `admin` 
* Contraseña: `password` 

---

## 🎯 Filosofía del Proyecto

GES **no intenta competir con grandes ERPs educativos online**.

Su propósito es:

* Ser **simple**
* Ser **robusto**
* Ser **comprensible**
* Resolver el **80% de los problemas reales** de un colegio local

---

## 🚀 Roadmap (Simplificado)

* [x] MVP funcional completo
* [x] Arquitectura limpia
* [x] UI base completa
* [ ] Pruebas extendidas (QA)
* [ ] Optimización de MainView y navegación
* [ ] Empaquetado instalable
* [ ] Versión estable v1.0

---

## 🧠 Autor

**Luis Rafael Eyoma**
Desarrollador de Software (Python)
Fundador de **Xenon.py**
Guinea Ecuatorial 🇬🇶

> Construyendo soberanía tecnológica desde contextos reales.

---

## 📄 Licencia

Proyecto en desarrollo.
Licencia por definir tras la versión estable.

---

⚠️ **Nota final:**
Este proyecto está en evolución activa. Cualquier feedback técnico es bienvenido.