# GES - Sistema de Gestión Escolar (Nuevo Diseño)

Sistema de gestión escolar offline-first para escuelas locales de Guinea Ecuatorial.

## 🏗️ Arquitectura del Dominio

### Entidades Principales

- **School**: Institución educativa
- **User**: Usuarios del sistema (admin, secretary, teacher)
- **Student**: Estudiantes matriculados
- **Tutor**: Tutores/responsables de estudiantes
- **AcademicYear**: Años académicos con configuración
- **Grade**: Niveles/grados educativos
- **Course**: Asignaturas/cursos
- **Classroom**: Aulas físicas
- **Enrollment**: Matrículas de estudiantes
- **Payment**: Pagos y cobros

## 📁 Estructura del Proyecto

```
ges_proy/
├── app/
│   └── domain/           # Entidades del dominio (puras)
│       └── entities.py   # School, User, Student, etc.
├── database/
│   ├── models/          # Modelos SQLAlchemy
│   │   ├── base.py      # Base común
│   │   ├── school.py    # School, Grade, Course, etc.
│   │   ├── person.py    # Person, User, Student, Tutor
│   │   └── enrollment.py # Enrollment, Payment
│   └── db.py           # Configuración y gestión
├── test_database.py     # Pruebas de la base de datos
└── requirements.txt     # Dependencias
```

## 🚀 Instalación y Uso

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Probar base de datos:**
```bash
python test_database.py
```

3. **Datos por defecto:**
- Usuario: `admin`
- Contraseña: `password`

## 🔧 Características Implementadas

### ✅ Núcleo del Dominio
- Entidades completas con validaciones
- Enums para estados y roles
- Relaciones claras entre entidades
- Propiedades calculadas útiles

### ✅ Base de Datos
- SQLAlchemy con SQLite
- Modelo relacional completo
- Migraciones automáticas
- Datos de ejemplo

### ✅ Gestión de Matrículas
- Sistema de matrícula por año académico
- Asignación de tutores
- Estados de matrícula (active, inactive, graduated)

### ✅ Sistema de Pagos
- Configuración de tarifas por año
- Estados de pago (pending, paid, overdue)
- Control de fechas de vencimiento

## 📋 Decisiones de Diseño

1. **Base SQLAlchemy única**: Evita conflictos de relaciones
2. **Entidades puras**: Separación clara del dominio
3. **Enums tipados**: Seguridad en estados y roles
4. **IDs automáticos**: Generación automática de códigos
5. **Relaciones lazy**: Optimización de consultas

## 🎯 Próximos Pasos

1. **Servicios de negocio**: Lógica de matrícula y pagos
2. **Repositorios**: Acceso a datos especializado
3. **UI Moderna**: CustomTkinter para gestión
4. **Importación Excel**: Carga masiva de datos
5. **Reportes**: Estadísticas y exportación

## 🧪 Testing

El sistema incluye pruebas completas:
- ✅ Creación de base de datos
- ✅ Operaciones CRUD básicas
- ✅ Creación de entidades
- ✅ Relaciones entre modelos

## 📊 Datos de Ejemplo

El sistema crea automáticamente:
- 1 escuela (Colegio Ejemplo)
- 1 año académico (2024-2025)
- 1 grado (1º Primaria)
- 1 aula (A-101)
- 1 asignatura (Matemáticas)
- 1 usuario admin

## 🔐 Seguridad

- Hash de contraseñas (MD5 básico, mejorar en producción)
- Roles de usuario definidos
- Validación de estados
- Control de acceso por rol