# Decisiones Arquitecturales y de Diseño - Módulo de Importación de Estudiantes

## Fecha
Mayo 14, 2026

## Contexto
Durante el desarrollo del módulo de importación de estudiantes desde Excel para el sistema GES (Gestión Educativa), se tomaron varias decisiones críticas que afectan la arquitectura, funcionalidad y mantenibilidad del sistema.

## Decisiones Tomadas

### 1. Arquitectura de Importación
**Decisión**: Implementar una arquitectura de tres capas (UI → Servicio → Repositorio) con procesamiento asíncrono.

**Razones**:
- Separación clara de responsabilidades
- Procesamiento en background para evitar bloqueo de UI
- Reutilización de servicios existentes
- Facilita testing y mantenimiento

**Alternativas Consideradas**:
- Procesamiento síncrono directo desde UI
- Arquitectura de dos capas (UI → Repositorio)

### 2. Campos Obligatorios en Estudiantes
**Decisión**: Hacer obligatorio el campo "Nivel" (Preescolar, Primaria, Secundaria, Bachillerato) para todos los estudiantes.

**Razones**:
- Requisito de negocio: agrupación por nivel educativo
- Integridad de datos: evita estudiantes sin clasificación
- Facilita reportes y análisis por nivel

**Impacto**:
- Modificación de esquema de base de datos
- Actualización de formularios UI
- Validación en importación Excel

### 3. Manejo de Precios de Matrícula
**Decisión**: Establecer precios fijos por nivel educativo en la inicialización del sistema.

**Precios Definidos**:
- Preescolar: 50,000 FCFA
- Primaria: 75,000 FCFA
- Secundaria: 100,000 FCFA
- Bachillerato: 125,000 FCFA

**Razones**:
- Simplifica cálculos financieros
- Proporciona valores por defecto operativos
- Puede ser modificado por administradores posteriormente

### 4. Validación de Datos Excel
**Decisión**: Implementar validación estricta con mapeo flexible de columnas.

**Características**:
- Columnas requeridas: nombre, apellido, nivel, curso, aula, turno, año escolar
- Mapeo de aliases para compatibilidad (ej: "clase" → "aula", "fechanac" → "fechanacimiento")
- Validación de tipos de datos y rangos

**Razones**:
- Robustez contra errores de usuario
- Compatibilidad con diferentes formatos de Excel
- Prevención de datos corruptos

### 5. Manejo de Errores en UI
**Decisión**: Implementar manejo seguro de excepciones en componentes Tkinter, especialmente DoubleVar.

**Ejemplo Crítico**:
- En calendar_view.py: Validar DoubleVar antes de .get() para evitar TclError
- En finance_view.py: Mejorar selección de estudiantes con IDs ocultos

**Razones**:
- Experiencia de usuario fluida
- Prevención de crashes por entradas inválidas
- Logging adecuado de errores

### 6. Estructura de Base de Datos
**Decisión**: Extender tabla students con columna nivel y migración automática.

**Cambios**:
- ALTER TABLE students ADD COLUMN nivel TEXT
- Inserción de precios por defecto en enrollment_prices

**Razones**:
- Evolución incremental del esquema
- Compatibilidad con datos existentes
- Mantenimiento de integridad referencial

### 7. Patrón de Nombres de Archivos
**Decisión**: Seguir convención snake_case para archivos Python y estructura jerárquica clara.

**Estructura Adoptada**:
```
services/
  student_service.py
  student_import_service.py
ui/
  students_view.py
  calendar_view.py
utils/importers/
  excel_student_importer.py
```

**Razones**:
- Consistencia con estándares Python
- Facilita navegación y mantenimiento
- Escalabilidad del proyecto

## Consecuencias

### Positivas
- Sistema más robusto y mantenible
- Mejor experiencia de usuario
- Datos más consistentes
- Arquitectura escalable

### Riesgos Identificados
- Complejidad añadida por validaciones estrictas
- Posibles conflictos con datos existentes
- Dependencia de formato Excel específico

## Próximas Revisiones
- Evaluar impacto en performance con grandes volúmenes de datos
- Considerar internacionalización de mensajes de error
- Revisar necesidad de campos adicionales en estudiantes</content>
<parameter name="filePath">c:\Users\ideapad\Documents\LRE\ges_proy\docs\decisions\decisions_import_module.md