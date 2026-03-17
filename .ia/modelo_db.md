Si la base está mal pensada, todo GES se tambalea.
Si está bien diseñada, el 50% del producto ya está ganado.

Voy a diseñarla con estos principios:

* ✔ Solo lo necesario para el MVP
* ✔ Preparada para LAN
* ✔ Preparada para crecimiento
* ✔ Sin tablas innecesarias
* ✔ Sin sobreingeniería

---

# 📦 MODELO DE BASE DE DATOS — GES MVP

Base: **SQLite**

---

# 1️⃣ TABLAS ESTRUCTURALES (Organización)

## 🏫 schools

(Solo 1 registro por instalación)

| Campo       | Tipo       | Descripción |
| ----------- | ---------- | ----------- |
| id          | INTEGER PK |             |
| name        | TEXT       |             |
| city        | TEXT       |             |
| year_active | INTEGER    |             |
| created_at  | DATETIME   |             |

---

## 👥 users

(Directiva, secretaria, usuarios)

| Campo         | Tipo        |
| ------------- | ----------- |
| id            | INTEGER PK  |
| username      | TEXT UNIQUE |
| password_hash | TEXT        |
| role_id       | INTEGER FK  |
| is_active     | BOOLEAN     |
| created_at    | DATETIME    |

---

## 🎭 roles

| Campo       | Tipo        |
| ----------- | ----------- |
| id          | INTEGER PK  |
| name        | TEXT        |
| permissions | TEXT (JSON) |

Permisos en JSON:

```json
{
  "view_dashboard": true,
  "edit_students": false,
  "view_finances": true
}
```

---

# 2️⃣ ESTRUCTURA ACADÉMICA

## 🎓 levels

(Ej: Primaria, Secundaria, Bachillerato)

| id | name |

---

## 📚 grades

(1º, 2º, 3º…)

| id | level_id | name |

---

## 🏫 classrooms

| id | grade_id | name | shift |

shift: "Mañana" / "Tarde"

---

## 📖 subjects

| id | name |

---

## 👨‍🏫 teachers

| id | name | subject_id |

---

# 3️⃣ ESTUDIANTES

## 👨‍🎓 students

| Campo             | Tipo       |
| ----------------- | ---------- |
| id                | INTEGER PK |
| first_name        | TEXT       |
| last_name         | TEXT       |
| classroom_id      | INTEGER FK |
| enrollment_status | TEXT       |
| tutor_name        | TEXT       |
| created_at        | DATETIME   |

enrollment_status:

* activo
* retirado
* graduado

---

# 4️⃣ NOTAS

## 📝 scores

| Campo          | Tipo            |
| -------------- | --------------- |
| id             | INTEGER PK      |
| student_id     | FK              |
| subject_id     | FK              |
| teacher_id     | FK              |
| trimester      | INTEGER (1,2,3) |
| score          | REAL            |
| recovery_score | REAL            |
| academic_year  | INTEGER         |

---

# 5️⃣ PAGOS

## 💰 payments

| Campo          | Tipo       |
| -------------- | ---------- |
| id             | INTEGER PK |
| student_id     | FK         |
| amount_due     | REAL       |
| amount_paid    | REAL       |
| due_date       | DATE       |
| status         | TEXT       |
| calendar_group | TEXT       |

status:

* pendiente
* pagado
* retrasado

---

# 6️⃣ ALERTAS

## ⚠ alerts

| id | type | reference_id | message | created_at |

type:

* rendimiento
* morosidad
* abandono

---

# 7️⃣ HISTORIAL

## 📜 history

| id | user_id | action | timestamp |

Para trazabilidad básica.

---

# 🔁 RELACIONES CLAVE

* Un level → muchos grados
* Un grade → muchas classrooms
* Una classroom → muchos students
* Un student → muchos scores
* Un student → muchos payments
* Un role → muchos users

---

# 🧠 Por qué este modelo es correcto

✔ Permite análisis por:

* nivel
* grado
* aula
* turno
* profesor
* materia
* trimestre

✔ Permite detectar:

* materias con suspensos altos
* profesores con patrón repetido
* rendimiento por turno
* abandono
* morosidad agrupada

✔ Funciona en standalone y servidor sin cambios.

---

# ⚠ Lo que NO incluí a propósito

* Tablas duplicadas
* Configuración innecesaria
* Sistemas complejos de auditoría
* Relaciones redundantes
* Automatización excesiva

