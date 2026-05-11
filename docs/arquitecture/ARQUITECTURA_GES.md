# 🏗️ ARQUITECTURA GES (Sistema de Gestión Escolar) - ACTUALIZADO v2.0

**Documento de Análisis Arquitectónico - Versión 2.0 (Arquitectura Híbrida)**  
**Generado:** Mayo 2026  
**Estado del Proyecto:** Refactorización completada - Multi-modo operativo  
**Análisis:** Basado en código real del proyecto

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Árbol Simplificado del Proyecto](#2-árbol-simplificado-del-proyecto)
3. [Diagrama Arquitectónico Principal](#3-diagrama-arquitectónico-principal)
4. [Flujos de Operación](#4-flujos-de-operación)
5. [Capas Identificadas](#5-capas-identificadas)
6. [Integraciones API REST](#6-integraciones-api-rest)
7. [Base de Datos](#7-base-de-datos)
8. [Relaciones Críticas](#8-relaciones-críticas)
9. [Riesgos Arquitectónicos](#9-riesgos-arquitectónicos)
10. [Propuestas de Mejora](#10-propuestas-de-mejora)

---

## 1. Resumen Ejecutivo

### 🎯 Tipo de Arquitectura Detectada

**Arquitectura Híbrida Multi-Modo: Desktop + API REST**

El proyecto soporta **3 modos de ejecución simultáneamente** sin código duplicado:

| Modo | Tipo | Punto Entrada | Uso |
|------|------|---------------|-----|
| **NORMAL** | Desktop Standalone | `main.py` → GESApplication | Instalación local sin red |
| **SERVER** | FastAPI REST | `api/server.py` (uvicorn) | Servidor LAN centralizado |
| **CLIENT** | Desktop + Remoto | `main.py` (GESApiClient) | Cliente conectado a servidor |

### 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Uso |
|-----------|-----------|-----|
| **GUI Desktop** | Tkinter (built-in) | Interfaz local |
| **Framework REST** | FastAPI | Servidor API |
| **Servidor ASGI** | Uvicorn | Ejecutor FastAPI |
| **Cliente HTTP** | requests | Modo client |
| **Base de Datos** | SQLite | Persistencia local |
| **Validación** | Pydantic | Esquemas API |
| **Reportes** | ReportLab | PDF generation |
| **Excel** | OpenPyXL | Importar/exportar |
| **Lenguaje** | Python | 3.10+ |

### 📐 Patrón Arquitectónico Principal

```
┌──────────────────────────────────────────────────────┐
│     Repository Pattern + Service Layer (reutilizable) │
│  Usado por: Desktop + API REST + Cliente Remoto       │
├──────────────────────────────────────────────────────┤
│  Capa UI    ← → Capa Services ← → Capa Repository     │
│  Desktop    ← → FastAPI/Client ← → SQLite Local       │
└──────────────────────────────────────────────────────┘
```

**Ventaja clave:** Un único código de Services y Repository usado por 3 entornos diferentes.

---

## 2. Árbol Simplificado del Proyecto

```
ges_proy/                                    ← Raíz del proyecto
│
├── 📄 main.py                              ← 🔴 PUNTO DE ENTRADA (Desktop/Client)
├── 📄 config.py                            ← Constantes (rutas, puertos)
├── 📄 config.json                          ← Configuración runtime (modo, IP, puerto)
│
├── 📁 api/                                 ← 🔴 API REST (FastAPI)
│   ├── server.py                           → Punto entrada FastAPI + middleware CORS
│   ├── auth_manager.py                     → Tokens JWT Bearer (24h TTL)
│   ├── routes_auth.py                      → POST /auth/login, /auth/logout
│   ├── routes_students.py                  → GET/POST /students/
│   ├── routes_dashboard.py                 → GET /dashboard/ (académico + financiero)
│   └── __init__.py
│
├── 📁 ui/                                  ← 🎨 INTERFAZ DE USUARIO (Tkinter)
│   ├── login.py                            → Ventana de login (local o remoto)
│   ├── dashboard.py                        → Panel principal
│   ├── students_view.py                    → CRUD estudiantes
│   ├── academic_view.py                    → Calificaciones
│   ├── academic_structure_view.py          → Grados, materias, aulas
│   ├── finance_view.py                     → Pagos y cuotas
│   ├── calendar_view.py                    → Calendario académico
│   ├── reports_view.py                     → Reportes PDF
│   ├── settings_view.py                    → Configuración
│   └── __init__.py
│
├── 📁 services/                            ← 💼 LÓGICA DE NEGOCIO (reutilizada)
│   ├── student_service.py                  → CRUD estudiantes + validaciones
│   ├── academic_service.py                 → Cálculos académicos + alertas
│   ├── finance_service.py                  → Pagos, cuotas, deuda + alertas
│   ├── report_service.py                   → Generación reportes (PDF, Excel)
│   ├── api_client.py                       → Cliente HTTP (para modo client)
│   └── __init__.py
│
├── 📁 database/                            ← 🗃️ ACCESO A DATOS
│   ├── models.py                           → Creación de tablas (DDL)
│   ├── repository.py                       → BaseRepository + CRUD genérico
│   ├── connection.py                       → Context manager SQLite
│   └── __init__.py
│
├── 📁 core/                                ← ⚙️ LÓGICA PURA (sin dependencias)
│   ├── engine.py                           → Cálculos académicos/financieros
│   │   ├── AcademicMetrics                 → Métricas académicas
│   │   ├── FinancialMetrics                → Métricas financieras
│   │   ├── calculate_student_average()     → Promedio trimestral
│   │   ├── generate_alert()                → Alertas
│   │   └── ...funciones puras
│   └── __init__.py
│
├── 📁 utils/                               ← 🔧 UTILIDADES
│   ├── helpers.py                          → Funciones compartidas
│   ├── excel_importer.py                   → Importar estudiantes
│   └── __init__.py
│
├── 📁 tests/                               ← ✅ PRUEBAS
│   ├── test_services_basic.py
│   ├── test_repository.py
│   ├── test_integration_basic.py
│   └── test_integration.py
│
├── 📁 data/                                ← 💾 PERSISTENCIA
│   └── ges.db                              → SQLite (archivo único)
│
├── 📁 docs/                                ← 📚 DOCUMENTACIÓN
│   └── arquitecture/                       → Análisis arquitectónico
│       └── ARQUITECTURA_GES.md             → Este archivo
│
├── 📁 app/                                 ← ⚠️ ESTRUCTURA HEREDADA (deprecada)
├── 📁 .venv/                               ← Entorno virtual
├── 📁 .git/                                ← Control versiones
└── requirements.txt                        ← Dependencias Python
```

---

## 3. Diagrama Arquitectónico Principal

```mermaid
graph TB
    subgraph "👤 USUARIOS"
        A["Usuario Local<br/>(Instalación Desktop)"]
        B["Usuario en LAN<br/>(Cliente Remoto)"]
        C["Aplicación Externa<br/>(Cliente HTTP)"]
    end
    
    subgraph "🎨 PRESENTATION LAYER"
        UI_LOGIN["LoginWindow<br/>(Tkinter)"]
        UI_DASH["DashboardWindow<br/>(Tkinter)"]
        UI_VIEWS["Views<br/>(Students, Academic,<br/>Finance, Reports)"]
        
        A -->|inicia| UI_LOGIN
        B -->|conecta remoto| UI_LOGIN
        UI_LOGIN -->|autentica| UI_DASH
        UI_DASH -->|navega| UI_VIEWS
    end
    
    subgraph "🔐 AUTHENTICATION"
        AUTH_LOCAL["AuthLocal<br/>(SHA-256)"]
        AUTH_API["AuthAPI<br/>(JWT Bearer)"]
        
        A -->|modo normal| AUTH_LOCAL
        B -->|modo client| AUTH_API
        C -->|modo server| AUTH_API
    end
    
    subgraph "💼 SERVICE LAYER (reutilizable)"
        STUDENT["StudentService<br/>(CRUD + validaciones)"]
        ACADEMIC["AcademicService<br/>(Cálculos notas)"]
        FINANCE["FinanceService<br/>(Pagos + alertas)"]
        REPORT["ReportService<br/>(PDF + Excel)"]
        
        UI_VIEWS -->|invoca| STUDENT & ACADEMIC & FINANCE & REPORT
    end
    
    subgraph "⚙️ CORE ENGINE (lógica pura)"
        CALC["CoreEngine<br/>(cálculos determinísticos<br/>sin BD ni red)"]
        
        ACADEMIC -->|usa| CALC
        FINANCE -->|usa| CALC
    end
    
    subgraph "🗄️ REPOSITORY LAYER"
        BASE_REPO["BaseRepository<br/>(CRUD genérico)"]
        REPO["Repositorios específicos<br/>(User, Student,<br/>Score, Payment)"]
        
        STUDENT & ACADEMIC & FINANCE & REPORT -->|usa| REPO
        REPO -->|hereda de| BASE_REPO
    end
    
    subgraph "📡 API REST LAYER (FastAPI)"
        API_AUTH["/auth/login<br/>POST - Bearer Token"]
        API_STUDENTS["/students<br/>GET/POST/PUT/DELETE"]
        API_DASH["/dashboard<br/>GET - Métricas"]
        
        C -->|HTTP| API_AUTH & API_STUDENTS & API_DASH
        API_AUTH & API_STUDENTS & API_DASH -->|usa| STUDENT & ACADEMIC & FINANCE
    end
    
    subgraph "📡 HTTP CLIENT (modo client)"
        API_CLIENT["GESApiClient<br/>(requests)"]
        
        B -->|invoca| API_CLIENT
        API_CLIENT -->|HTTP| FastAPI["FastAPI Server<br/>(puerto 8000)"]
        FastAPI -->|usa| API_AUTH & API_STUDENTS & API_DASH
    end
    
    subgraph "🗃️ DATABASE LAYER"
        CONNECTION["SQLite Connection<br/>(context manager)"]
        MODELS["Database Models<br/>(16 tablas)"]
        
        BASE_REPO -->|usa| CONNECTION
        CONNECTION -->|mapea| MODELS
    end
    
    subgraph "💾 PERSISTENCE"
        SQLITE["SQLite DB<br/>(data/ges.db)"]
        
        MODELS -->|SQL| SQLITE
    end
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style UI_LOGIN fill:#fff3e0
    style UI_DASH fill:#fff3e0
    style UI_VIEWS fill:#fff3e0
    style STUDENT fill:#e8f5e9
    style ACADEMIC fill:#e8f5e9
    style FINANCE fill:#e8f5e9
    style REPORT fill:#e8f5e9
    style CALC fill:#fffde7
    style BASE_REPO fill:#fce4ec
    style REPO fill:#fce4ec
    style API_AUTH fill:#c8e6c9
    style API_STUDENTS fill:#c8e6c9
    style API_DASH fill:#c8e6c9
    style API_CLIENT fill:#ffccbc
    style FastAPI fill:#ffccbc
    style CONNECTION fill:#b3e5fc
    style MODELS fill:#b3e5fc
    style SQLITE fill:#ffccbc
```

---

## 4. Flujos de Operación

### 4.1 Modo NORMAL (Desktop Standalone)

```mermaid
sequenceDiagram
    participant User
    participant UI as Tkinter UI
    participant Services
    participant Repository
    participant SQLite
    
    User ->> UI: Inicia aplicación
    UI ->> Services: AuthService.authenticate()
    Services ->> Repository: UserRepository.find_by_username()
    Repository ->> SQLite: SELECT * FROM users
    SQLite -->> Repository: user_data
    Repository -->> Services: usuario
    Services -->> UI: login exitoso
    UI ->> UI: mostrar Dashboard
    User ->> UI: Navega a Estudiantes
    UI ->> Services: StudentService.get_all()
    Services ->> Repository: StudentRepository.get_all()
    Repository ->> SQLite: SELECT * FROM students
    SQLite -->> Repository: [students]
    Repository -->> Services: [Student objects]
    Services -->> UI: mostrar lista
```

### 4.2 Modo CLIENT (Remoto vía HTTP)

```mermaid
sequenceDiagram
    participant User
    participant ClientUI as Client UI<br/>(local)
    participant APIClient as GESApiClient<br/>(HTTP)
    participant FastAPI as FastAPI Server<br/>(LAN)
    participant Services as Services +<br/>Repository
    participant RemoteSQLite as SQLite<br/>(servidor)
    
    User ->> ClientUI: Ingresa credenciales
    ClientUI ->> APIClient: login(username, password)
    APIClient ->> FastAPI: POST /auth/login
    FastAPI ->> Services: AuthService.authenticate()
    Services ->> RemoteSQLite: queries
    RemoteSQLite -->> Services: datos
    Services -->> FastAPI: válido
    FastAPI ->> FastAPI: generar JWT token (24h)
    FastAPI -->> APIClient: {token, user_data}
    APIClient ->> APIClient: guardar token
    APIClient -->> ClientUI: login exitoso
    ClientUI ->> ClientUI: mostrar Dashboard
    User ->> ClientUI: solicita estudiantes
    ClientUI ->> APIClient: GET /students/
    APIClient ->> FastAPI: GET /students/<br/>Authorization: Bearer {token}
    FastAPI ->> Services: StudentService.get_all()
    Services ->> RemoteSQLite: SELECT * FROM students
    RemoteSQLite -->> Services: [students]
    Services -->> FastAPI: [data]
    FastAPI -->> APIClient: [students JSON]
    APIClient -->> ClientUI: mostrar estudiantes
```

### 4.3 Modo SERVER (API Pura)

```mermaid
sequenceDiagram
    participant Client as Cliente Externo<br/>(Postman, Móvil)
    participant FastAPI as FastAPI Server
    participant AuthMgr as auth_manager<br/>(JWT)
    participant Services
    participant Repository
    participant SQLite
    
    Client ->> FastAPI: POST /auth/login<br/>{username, password}
    FastAPI ->> AuthMgr: authenticate()
    AuthMgr ->> Services: validar usuario
    Services ->> Repository: queries
    Repository ->> SQLite: SELECT * FROM users
    SQLite -->> Repository: user
    Repository -->> Services: user_object
    Services -->> AuthMgr: válido
    AuthMgr ->> AuthMgr: crear JWT token
    AuthMgr -->> FastAPI: token + metadata
    FastAPI -->> Client: {token, expires_at}
    Client ->> FastAPI: GET /students/<br/>Authorization: Bearer {token}
    FastAPI ->> AuthMgr: validar_token()
    AuthMgr -->> FastAPI: válido
    FastAPI ->> Services: StudentService.get_all()
    Services ->> Repository: CRUD queries
    Repository ->> SQLite: SELECT * FROM students
    SQLite -->> Repository: [students]
    Repository -->> Services: [objects]
    Services -->> FastAPI: [data]
    FastAPI -->> Client: [students JSON]
```

---

## 5. Capas Identificadas

### 5.1 Capa de Presentación (UI)

**Ubicación:** `ui/` (8 vistas principales - Tkinter)

| Componente | Responsabilidad |
|-----------|-----------------|
| **LoginWindow** | Autenticación (local o remota vía API) |
| **DashboardWindow** | Resumen, alertas, métricas |
| **StudentsView** | CRUD estudiantes, búsqueda |
| **AcademicView** | Calificaciones por trimestre |
| **AcademicStructureView** | Grados, materias, aulas |
| **FinanceView** | Pagos, cuotas, deuda |
| **CalendarView** | Calendario académico |
| **ReportsView** | Generación reportes PDF/Excel |
| **SettingsView** | Configuración del sistema |

---

### 5.2 Capa de Servicios (Lógica de Negocio)

**Ubicación:** `services/` (reutilizable por Desktop + API)

| Servicio | Responsabilidad |
|----------|-----------------|
| **StudentService** | CRUD + validaciones email/edad + búsqueda |
| **AcademicService** | Promedios, alertas rendimiento |
| **FinanceService** | Pagos, deuda, alertas morosidad |
| **ReportService** | Reportes PDF/Excel |
| **GESApiClient** | Cliente HTTP (modo client) |

**Características:**
- ✅ Orquestación de operaciones
- ✅ Validaciones de negocio
- ✅ Generación de alertas
- ✅ Reutilizable en Desktop + API REST

---

### 5.3 Core Engine (Lógica Pura)

**Ubicación:** `core/engine.py`

**Ventajas:**
- ⚙️ Sin dependencias externas (no importa BD, HTTP)
- ⚙️ Funciones matemáticas determinísticas
- ⚙️ Fácil testing unitario

**Componentes:**
```python
AcademicMetrics:
    - average: float
    - passed_subjects: int
    - failed_subjects: int
    - recovery_count: int

FinancialMetrics:
    - total_due: float
    - total_paid: float
    - outstanding: float
    - days_overdue: int

# Cálculos
- calculate_student_average(scores)
- generate_academic_alert(metrics)
- generate_financial_alert(metrics)
```

---

### 5.4 Capa de Repositorios (Acceso a Datos)

**Ubicación:** `database/repository.py`

**Patrón:** Repository genérico + específicos

```python
class BaseRepository:
    - create(model) → id
    - get(id) → object
    - get_all() → [objects]
    - update(id, data) → bool
    - delete(id) → bool

class UserRepository:
    - find_by_username(username) → User
    - authenticate(username, hash) → bool

class StudentRepository:
    - find_by_aula(aula_id) → [Student]
    - search(name, grade) → [Student]
    - is_enrolled(student_id, year_id) → bool
```

---

### 5.5 Capa de Base de Datos

**Ubicación:** `database/`

| Archivo | Responsabilidad |
|---------|-----------------|
| **models.py** | Creación DDL (16 tablas) |
| **repository.py** | CRUD + queries |
| **connection.py** | Context manager SQLite |

---

### 5.6 Capa de API REST

**Ubicación:** `api/` (FastAPI + Uvicorn)

| Componente | Responsabilidad |
|-----------|-----------------|
| **server.py** | Inicializa FastAPI + CORS + routers |
| **auth_manager.py** | JWT tokens (generar, validar, limpiar) |
| **routes_auth.py** | `/auth/login`, `/auth/logout` |
| **routes_students.py** | `/students/*` CRUD |
| **routes_dashboard.py** | `/dashboard/` métricas |

**Endpoints principales:**
```
POST   /auth/login              → {token, user_data, expires_at}
POST   /auth/logout             → {message}
GET    /students/               → [students]
GET    /students/{id}           → student_details
POST   /students/               → create_student
GET    /dashboard/              → {academic_metrics, financial_metrics}
GET    /health                  → {status, timestamp}
```

---

## 6. Integraciones API REST

### 6.1 Flujo de Autenticación JWT

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant AuthMgr as auth_manager
    participant Storage as Session Storage
    
    Client ->> FastAPI: POST /auth/login<br/>{username, password}
    FastAPI ->> AuthMgr: authenticate(username, password)
    AuthMgr ->> AuthMgr: hash_password(password)
    AuthMgr ->> AuthMgr: buscar usuario en BD
    AuthMgr ->> AuthMgr: validar hash
    alt credenciales válidas
        AuthMgr ->> AuthMgr: crear JWT token<br/>(exp: +24h)
        AuthMgr ->> Storage: guardar token
        AuthMgr -->> FastAPI: {token, expires_at}
        FastAPI -->> Client: {token, user_data, expires_at}
    else credenciales inválidas
        AuthMgr -->> FastAPI: error
        FastAPI -->> Client: {error: "invalid credentials"}
    end
    
    Client ->> FastAPI: GET /students/<br/>Authorization: Bearer {token}
    FastAPI ->> AuthMgr: validar_token(token)
    AuthMgr ->> Storage: obtener token
    AuthMgr ->> AuthMgr: verificar expiración
    alt token válido
        AuthMgr -->> FastAPI: válido
        FastAPI ->> FastAPI: ejecutar endpoint
    else token expirado/inválido
        AuthMgr -->> FastAPI: inválido
        FastAPI -->> Client: {error: "unauthorized"}
    end
```

### 6.2 Middleware CORS

```python
# api/server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 🔥 ABIERTO (cambiar en producción)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

## 7. Base de Datos

### 7.1 Esquema de 16 Tablas

```sql
-- Estructura Escolar (4)
schools                 -- Información institucional
levels                  -- Primaria, Secundaria
grades                  -- Niveles (1ro, 2do, 3ro)
classrooms              -- Aulas específicas

-- Usuarios (2)
users                   -- Admin, Secretaria, Profesor
roles                   -- ADMIN, SECRETARY, TEACHER

-- Académica (3)
subjects                -- Materias
teachers                -- Profesores
scores                  -- Calificaciones (trimestre 1-3)

-- Financiera (4)
enrollment_prices       -- Costo por grado/año
payments                -- Pagos realizados
payment_calendars       -- Plan de pagos
payment_installments    -- Cada cuota individual

-- Sistema (3)
students                -- Estudiantes (estado: activo, retirado, graduado)
student_calendars       -- Calendario por estudiante
alerts                  -- Alertas generadas
```

### 7.2 Ubicación Física

```
data/
└── ges.db              ← SQLite archivo único
                        ← 16 tablas
                        ← Accesible: modo normal, server, client
```

---

## 8. Relaciones Críticas

### 8.1 Módulos Críticos (Sin estos = No funciona)

| Módulo | Razón | Fallo |
|--------|-------|-------|
| **database/connection.py** | Gestiona BD | ❌ No hay BD |
| **database/repository.py** | CRUD genérico | ❌ No se accede a datos |
| **config.py** | Constantes rutas | ❌ No hay rutas |
| **services/** | Lógica de negocio | ⚠️ Funcionalidad limitada |

### 8.2 Dependencias entre Capas

```
UI ↔ Services ← Repository ← Database
 ↑
 └─ FastAPI (cuando modo = "server" o "client")
```

### 8.3 Cuellos de Botella Potenciales

| Cuello | Impacto | Solución |
|--------|---------|----------|
| **SQLite monothread** | Múltiples clientes → lento | Migrar a PostgreSQL |
| **ReportLab PDF** | Reportes grandes lentos | Caché + async |
| **UI bloqueante** | Operaciones largas congelan | Threading |
| **JWT sin refresh** | Usuario desconectado 24h | Agregar refresh tokens |
| **CORS abierto** | Seguridad débil | Restricción IP |

---

## 9. Riesgos Arquitectónicos

### 🔴 CRÍTICOS

#### 1. Código Duplicado: `app/` vs Raíz

**Problema:**
```
├── app/domain/              ← DUPLICADO, DEPRECADO
├── app/repositories/        ← DUPLICADO, DEPRECADO
├── app/services/            ← DUPLICADO, DEPRECADO
├── app/ui/                  ← DUPLICADO, DEPRECADO

├── services/                ← ACTUAL (correcto)
├── database/repository.py   ← ACTUAL (correcto)
├── ui/                      ← ACTUAL (correcto)
```

**Impacto:** Confusión en qué código usar, mantenimiento duplicado

**Solución:** Eliminar `app/` completamente

---

#### 2. Configuración Hardcodeada

**Problema:**
```python
# En services/academic_service.py:
if average < 6.0:              # 🔥 Hardcodeado
    generate_alert(...)

# En services/finance_service.py:
if days_overdue > 30:          # 🔥 Hardcodeado
    generate_alert(...)
```

**Impacto:** Cambios requieren editar código + recompilar

**Solución:** Mover a `config.json` con schema validado

---

### 🟡 IMPORTANTES

#### 3. SHA-256 Débil para Contraseñas

**Problema:**
```python
# En ui/login.py:
hash = hashlib.sha256(password).hexdigest()  # 🔥 Sin salt, vulnerable
```

**Impacto:** Rainbow table attacks posibles

**Solución:** Usar bcrypt

---

#### 4. Sin Transacciones Explícitas

**Problema:**
```python
# Si falla aquí, datos inconsistentes:
payment = payment_repo.create(...)      # ✅
invoice = generate_invoice(...)         # ❌ Falla
```

**Impacto:** Matrículas sin cuotas, BD inconsistente

**Solución:** Context managers para transacciones

---

#### 5. CORS Abierto a Todos

**Problema:**
```python
# api/server.py:
allow_origins=["*"]  # 🔥 Cualquiera puede acceder
```

**Impacto:** Seguridad débil

**Solución:** Restricción a máquinas conocidas

---

### 🟢 MODERADOS

#### 6. Sin Logging/Auditoría

**Problema:** No hay registro de cambios

**Impacto:** Imposible investigar modificaciones

---

#### 7. UI Bloqueante

**Problema:** Operaciones largas congelan Tkinter

**Impacto:** Experiencia de usuario pobre

**Solución:** Threading

---

#### 8. Sin Validación en API

**Problema:** FastAPI acepta cualquier JSON

**Impacto:** Datos malformados en BD

**Solución:** Pydantic schemas

---

## 10. Propuestas de Mejora

### Fase 1: Limpieza Inmediata (1-2 horas)

1. **Eliminar `app/`** - Mantener solo raíz
2. **Consolidar config** - `config.json` con schema Pydantic
3. **Actualizar imports** - Todos apunten a estructura correcta

### Fase 2: Seguridad (2-3 horas)

4. **SHA-256 → bcrypt** - Proteger contraseñas
5. **CORS restringido** - Solo máquinas autorizadas
6. **Validación Pydantic** - Esquemas en API

### Fase 3: Robustez (3-4 horas)

7. **Transacciones explícitas** - ACID garantizado
8. **Logging centralizado** - Auditoría de cambios
9. **Threading en UI** - Operaciones sin bloqueo

### Propuesta: Arquitectura Mejorada

```mermaid
graph TB
    subgraph "🎨 Presentation (Multi-modo)"
        UI["Desktop UI<br/>(Tkinter)"]
        API["FastAPI REST"]
    end
    
    subgraph "🏛️ Domain"
        DOMAIN["Domain Models<br/>(puro, sin BD)"]
        RULES["Business Rules<br/>(validaciones)"]
    end
    
    subgraph "💼 Application"
        SERVICES["Services<br/>(orquestación)"]
    end
    
    subgraph "🗄️ Data Access"
        REPO["Repository<br/>(transacciones)"]
        MODELS["SQLAlchemy Models"]
    end
    
    subgraph "⚙️ Infrastructure"
        CONFIG["Config<br/>(JSON + Pydantic)"]
        LOG["Logger<br/>(centralizado)"]
        AUDIT["Audit<br/>(cambios)"]
        SECURITY["Security<br/>(bcrypt + CORS)"]
    end
    
    subgraph "💾 Persistence"
        DB["SQLite | PostgreSQL"]
    end
    
    UI & API -->|usa| SERVICES
    SERVICES -->|crea| DOMAIN
    SERVICES -->|valida| RULES
    SERVICES -->|usa| REPO
    REPO -->|usa| MODELS
    MODELS -->|persiste| DB
    SERVICES & REPO -->|usa| CONFIG & LOG & AUDIT & SECURITY
    
    style UI fill:#fff3e0
    style API fill:#c8e6c9
    style SERVICES fill:#e8f5e9
    style REPO fill:#fce4ec
    style DB fill:#ffccbc
    style CONFIG fill:#f3e5f5
    style LOG fill:#f3e5f5
    style AUDIT fill:#f3e5f5
    style SECURITY fill:#f3e5f5
```

---

## 📊 Conclusiones

### ✅ Fortalezas Actuales

1. **Arquitectura Híbrida Única:** 3 modos sin código duplicado
2. **Separación Clara de Capas:** UI → Services → Repository → DB
3. **Reutilización Máxima:** Mismo código para Desktop + API + Client
4. **Core Engine Puro:** Lógica sin dependencias externas
5. **API REST Funcional:** FastAPI lista para múltiples clientes
6. **Configuración Flexible:** Modo configurable en runtime

### ⚠️ Mejoras Prioritarias

| Prioridad | Item | Tiempo | Beneficio |
|-----------|------|--------|-----------|
| 🔴 Alta | Eliminar `app/` | 30min | Claridad |
| 🔴 Alta | SHA-256 → bcrypt | 1h | Seguridad |
| 🟡 Media | CORS restringido | 30min | Seguridad |
| 🟡 Media | Pydantic schemas | 1.5h | Robustez |
| 🟡 Media | Transacciones | 2h | Consistencia |
| 🟢 Baja | Threading | 2h | UX |
| 🟢 Baja | Logging | 1h | Auditoría |

### 🎯 Recomendación

**La arquitectura es SÓLIDA y ESCALABLE.** El proyecto ha evolucionado correctamente hacia una estructura híbrida bien pensada.

**Acciones inmediatas (3 horas):**
1. Eliminar `app/` ✅
2. Agregar bcrypt ✅
3. Pydantic schemas ✅

Con esto, estará **production-ready**.

---

**Documento:** Mayo 2026  
**Versión:** 2.0 (Actualizado - Arquitectura Híbrida)  
**Estado:** ✅ Análisis Completo
