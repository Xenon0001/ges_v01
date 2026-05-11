Ahora vamos a **B) Arquitectura cliente-servidor concreta**.
Aquí definimos cómo funciona realmente GES en:

* 🖥 1 PC (modo Normal)
* 🖥🖥🖥 Red LAN (Servidor + Clientes)

---

# 🧠 ARQUITECTURA DEFINITIVA — GES

Principio rector:

> El núcleo de GES no sabe si está en standalone o en red.
> Solo cambia la forma en que se accede a los datos.

---

# 1️⃣ MODO NORMAL (1 PC)

Arquitectura:

```
UI  →  Servicios  →  SQLite local
```

* No hay servidor HTTP.
* No hay red.
* Acceso directo a la base de datos.
* Todo ocurre en el mismo proceso.

Ventajas:
✔ Simplicidad
✔ Menos errores
✔ Instalación rápida
✔ Ideal para centros con 1 PC

---

# 2️⃣ MODO SERVIDOR (Admin)

Arquitectura:

```
Clientes → API HTTP (FastAPI) → SQLite
```

En el PC servidor:

* Corre backend FastAPI
* Base de datos central
* Control de autenticación
* Control de roles
* Generación de código de enlace

El servidor escucha en:

```
http://IP_LOCAL:PUERTO
Ej: 192.168.1.10:8000
```

---

# 3️⃣ MODO CLIENTE (Usuario)

Arquitectura:

```
UI → HTTP requests → Servidor → DB
```

El cliente:

* No accede a SQLite
* No modifica estructura
* No define roles
* Solo consume endpoints permitidos

---

# 4️⃣ ¿Cómo decide GES qué modo usar?

En el primer arranque:

Si no existe archivo `config.json`:

→ Pantalla de selección:

* Servidor
* Usuario
* Normal

Se guarda algo así:

```json
{
  "mode": "server",
  "server_ip": null,
  "port": 8000
}
```

O:

```json
{
  "mode": "client",
  "server_ip": "192.168.1.10",
  "port": 8000
}
```

O:

```json
{
  "mode": "normal"
}
```

Cada inicio:

* Lee config
* Activa arquitectura correspondiente

---

# 5️⃣ Flujo de conexión LAN

## 🔹 Paso 1

Admin inicia modo servidor.
Se muestra:

* IP local
* Puerto
* Código de enlace (ej: 8432-AZ)

## 🔹 Paso 2

Cliente selecciona “Usuario”.
Introduce:

* IP
* Código de enlace

## 🔹 Paso 3

Servidor valida y crea usuario asociado.

---

# 6️⃣ Seguridad básica (sin exagerar)

Para MVP:

✔ Contraseñas con hash
✔ Token simple de sesión
✔ Roles verificados en backend
✔ No exponer endpoints sensibles

No necesitas:
❌ SSL en LAN
❌ Autenticación compleja OAuth
❌ Cifrado extremo

Simplicidad = estabilidad.

---

# 7️⃣ Manejo de fallos

Si cliente pierde conexión:

* Mostrar alerta
* No cerrar programa
* Permitir reintento

No implementar sincronización offline compleja.
Eso es Fase 3 futura.

---

# 8️⃣ Consumo real esperado

Servidor:

* Python: ~30MB
* FastAPI + Uvicorn: ~50MB
* SQLite: ~20MB
  Total: ~100MB

Cliente:

* UI + requests: ~60–100MB

En 8GB RAM → insignificante.

---

# 9️⃣ Decisión importante que tomamos ahora

No usaremos:

* PostgreSQL
* Docker
* Microservicios
* Redis
* Descubrimiento automático de red
* Sincronización distribuida

Usaremos:

* FastAPI
* SQLite
* Conexión manual por IP

Eso hace viable los 6 meses.

---

# 🔟 Resultado Arquitectónico

GES es:

* Aplicación híbrida
* Local-first
* LAN-capable
* Modular
* Escalable en fases

