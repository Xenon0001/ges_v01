Esta parte es crítica para que GES no se vuelva otro proyecto infinito.

---

# 🛠 D) PLAN DE EJECUCIÓN REAL — GES MVP

Regla:

> No se construye todo.
> Se construye en capas funcionales cerradas.

Nada de empezar 10 módulos a la vez.

---

# 🧭 FASE 1 — Núcleo funcional mínimo (Semanas 1–3)

Objetivo:
Que GES funcione en modo **Normal (1 PC)** completamente estable.

Sin red todavía.

---

## 🔹 Paso 1 — Estructura Base

Crear:

* Estructura de carpetas definitiva
* main.py
* config.py
* conexión SQLite
* modelo base

Sin UI compleja.
Solo pruebas en consola.

Meta:
✔ Crear usuario
✔ Insertar estudiante
✔ Registrar nota
✔ Registrar pago
✔ Consultar datos

Si esto falla → todo falla.

---

## 🔹 Paso 2 — Services + Core

Implementar:

* student_service
* academic_service
* finance_service

Y conectar con:

* repository
* engine

Probar cada servicio con pequeños scripts.

Sin interfaz todavía.

---

## 🔹 Paso 3 — UI mínima funcional

Crear:

* Login
* Dashboard simple
* Vista Estudiantes (CRUD básico)

Nada más.

Si aquí todo funciona → ya tienes un producto usable básico.

---

# 🧱 FASE 2 — Estabilidad y consistencia (Semanas 4–6)

Aquí no se agregan cosas nuevas.
Se refuerza lo que ya existe.

✔ Validaciones
✔ Manejo de errores
✔ Permisos
✔ Roles
✔ Formularios robustos
✔ Navegación limpia
✔ Pruebas manuales

---

# 🌐 FASE 3 — Activar modo Servidor (Semanas 7–10)

Aquí agregamos:

* FastAPI
* Endpoints básicos
* Autenticación
* Token simple
* Cliente HTTP en UI

Pero solo después de que modo normal sea sólido.

---

# 🎯 FASE 4 — Pulido profesional (Semanas 11–12)

* Exportación Excel
* Reportes PDF
* Optimización consultas
* Mejoras visuales
* Empaquetado ejecutable
* Archivo de instalación

---

# ⏳ Tiempo real estimado

Si trabajas 4–5 horas profundas al día:

3 meses disciplinados.

No 1 año.

