# 📘 DOCUMENTO DEL PROYECTO GES

# GES

## Sistema de Gestión Escolar Asistida

**Producto desarrollado por Xenon.py**

---

# 1️⃣ ¿Qué es GES?

GES es un sistema de gestión escolar asistida diseñado para centros educativos de Guinea Ecuatorial que buscan mejorar su organización, análisis académico y toma de decisiones sin depender de internet.

GES no es solo un sistema de registro.
Es una herramienta de análisis y control institucional.

Funciona completamente offline y puede operar:

* En un solo computador **modo Normal**
* En red local LAN con múltiples computadores **modo Servidor + Usuarios**

---

# 2️⃣ Propósito del Producto

El objetivo principal de GES es:

> Convertir los datos académicos y administrativos del centro en información clara para la Directiva.

GES permite:

* Evaluar rendimiento en tiempo real
* Detectar problemas académicos
* Controlar morosidad
* Analizar abandono
* Comparar niveles y turnos
* Generar informes listos para presentar

GES no espera al final del año para analizar.
Analiza mientras el año ocurre.

---

# 3️⃣ Arquitectura del Sistema

GES sigue una arquitectura híbrida:

## 🔹 Modo Normal (1 PC)

* Toda la base de datos es local.
* No existe servidor ni clientes.
* Funciona completamente independiente.

## 🔹 Modo Servidor (Admin)

* Un PC actúa como servidor.
* Controla la base de datos central.
* Define roles y permisos.
* Genera código de enlace.
* Gestiona usuarios.

## 🔹 Modo Usuario (Cliente)

* Se conecta al servidor por red local.
* Trabaja bajo permisos asignados.
* No controla la base de datos.
* Reporta cambios al servidor.

Importante:
Los clientes no dependen constantemente del servidor.
Se sincronizan cuando es necesario.

La configuración inicial se guarda en un archivo JSON local que define el rol del equipo.

---

# 4️⃣ Usuarios del Sistema

## 🎓 Directiva (Rol Superior)

* Acceso total
* Análisis completo
* Configuración
* Informes
* Gestión de roles

## 🗂 Secretaria

* Registro de estudiantes
* Gestión de notas
* Morosidad
* Importación Excel

## 👤 Usuario

* Permisos limitados según asignación

Los profesores no son usuarios directos.
Ellos entregan datos en Excel.

---

# 5️⃣ Estructura Funcional del Sistema

GES se organiza en módulos claros.

## 1. Dashboard (Estado del Centro)

Muestra:

* Rendimiento general trimestral
* Comparaciones
* Alertas
* Morosidad actual
* Indicadores clave

Objetivo:
Responder en 30 segundos:
“¿Cómo vamos?”

---

## 2. Análisis Académico

Permite:

* Comparar materias
* Comparar profesores
* Analizar por curso
* Analizar por turno
* Ver recuperación
* Detectar patrones

Objetivo:
Detectar dónde están los problemas reales.

---

## 3. Gestión de Alumnos

Incluye:

* Registro
* Historial
* Estado académico
* Abandono
* Migración
* Control de matrícula

---

## 4. Morosidad

Permite:

* Agrupar por tutor
* Calendarios de pago
* Alertas de retraso
* Seguimiento financiero básico

---

## 5. Boletines

Permite:

* Ingreso manual de notas
* Importación desde Excel
* Generación automática de boletines
* Cálculo automático de promedios

---

## 6. Informes

Generación automática de:

* Reportes trimestrales
* Estadísticas por grado
* Comparativas por turno
* Datos listos para impresión

---

# 6️⃣ MVP Definitivo

El MVP debe incluir:

1. Registro de estudiantes y personal
2. Importación Excel validada
3. Cálculo automático de rendimiento
4. Dashboard general
5. Comparación por materia y turno
6. Control básico de morosidad
7. Generación de PDF
8. Modo standalone funcional
9. Modo servidor LAN funcional

No incluye:

* IA avanzada
* Automatización PDF externa
* Plataforma online
* Mensajería
* App móvil

---

# 7️⃣ Número de Ventanas del MVP

Para mantener estabilidad:

1. Login
2. Configuración inicial (rol: servidor / usuario / normal)
3. Dashboard
4. Análisis académico
5. Gestión de alumnos
6. Morosidad
7. Boletines
8. Informes
9. Configuración / roles

Total aproximado: 8–9 ventanas principales.

Subventanas modales para formularios.

---

# 8️⃣ Lógica Interna de Funcionamiento

Flujo general:

Inicio →
Verificar configuración →
Cargar rol →
Conectar a DB (local o servidor) →
Cargar permisos →
Mostrar interfaz según rol →
Registrar datos →
Procesar cálculos →
Actualizar indicadores →
Guardar historial →
Generar informes

Todo bajo principio:

> Los datos entran una vez, el análisis es automático.

---

# 9️⃣ Qué ES GES realmente

GES es:

* Offline
* Adaptado al contexto local
* Cliente-servidor opcional
* Herramienta de análisis institucional
* Producto vendible
* Sistema pensado para pocos recursos

No es:

* Un ERP gigante
* Una plataforma online
* Un experimento técnico
* Un proyecto académico

---

# 🔟 Objetivo Estratégico Final

En 6 meses:

Tener un sistema estable que:

* Funcione en 1 PC
* Funcione en LAN
* Permita análisis reales
* Sea instalable
* Sea vendible

---

# 🎯 Declaración Final

GES no existe para demostrar que sabes programar.

Existe para:

* Ordenar centros escolares
* Dar claridad a la Directiva
* Profesionalizar la gestión educativa
* Contribuir al desarrollo tecnológico local

