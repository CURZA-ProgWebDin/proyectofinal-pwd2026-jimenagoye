# 🗂️ MACHETE — Examen Oral AcademiaPlus

> Resumen ultra-conciso para defender el proyecto · Vue 3 + Flask + MySQL + Docker

---

## 1. ARQUITECTURA (qué decir)

**Qué hace el proyecto:**
- Plataforma web de cursos con 3 roles: **alumno** (se inscribe), **creador** (publica módulos/clases) y **administrador**.
- Autenticación con **JWT** y rutas protegidas en backend y frontend.

**Los 3 componentes:**
- **Frontend** (Vue 3 + Pinia + Vue Router + Axios): interfaz, estado de sesión y navegación.
- **Backend** (Flask + Blueprints + SQLAlchemy): lógica de negocio, autenticación y API REST.
- **MySQL 8.0**: almacenamiento persistente con volumen.

**Cómo interactúan (clave del requisito):**
- El frontend **nunca habla con la BD directo**; solo se comunica con el backend vía HTTP (Axios → JSON).
- El backend usa SQLAlchemy como ORM para traducir objetos Python a SQL y consultar MySQL.
- Así la BD queda **accedida exclusivamente por el backend**, requisito obligatorio del proyecto.

**Estilo MVC en backend:**
- Separo **Routes** (HTTP), **Controllers** (lógica) y **Models** (ORM) dentro de cada Blueprint.
- Es arquitectura por capas / responsabilidad única trasladada al contexto web.

---

## 2. FLUJO DE DATOS (qué decir)

### Login — atraviesa todas las capas
- La vista dispara el submit → el **store de auth** llama a `login(email, password)` usando el servicio Axios.
- Axios hace `POST /api/auth/login` con baseURL `/api`; el **proxy de Vite** redirige a `backend:5000` y el interceptor prepara el header del token.
- El **controller** valida credenciales con bcrypt, consulta el usuario por email y, si es válido, genera el **JWT** con rol y nombre en los claims; responde JSON con `token` + `refresh_token` + `usuario`.
- El store guarda token y usuario en estado reactivo, los persiste en `localStorage` (sobrevive al refresh) y el guard de rutas ya permite entrar y navega a `/dashboard`.

### Catálogo público — GET /api/cursos/
- La vista de catálogo pide la lista de cursos; la ruta es pública (sin JWT).
- El controller arma la query con filtros opcionales (nivel, año, categoría, búsqueda con `ilike`) y pagina con `.paginate()`.
- SQLAlchemy ejecuta el SELECT en MySQL, serializa con `to_dict()` y el frontend renderiza las cards con `v-for`.

### Inscripción — requiere JWT + rol
- El usuario logueado pide inscribirse; el **interceptor de Axios** adjunta automáticamente `Authorization: Bearer <token>`.
- La ruta está protegida con `@jwt_required()` y `@rol_requerido("alumno")`: el decorador valida el JWT, busca el usuario y comprueba el rol (si no → 403).
- El controller evita el duplicado (restricción única alumno-curso), crea la inscripción y hace commit → responde 201 y la UI marca "inscrito".

### Gestión de contenido (creador/admin) — CRUD completo
- **Cursos**: crear, leer, actualizar y desactivar (`PUT`/`DELETE /cursos/:id`).
- **Módulos y clases**: crear, editar y eliminar (`POST`/`PUT`/`DELETE` anidados bajo el curso); el panel "Administrar curso" del detalle expone todo desde la UI.
- Los permisos se validan en el controller: solo el **creador del curso o un admin** puede modificarlo (mismo dueño → módulos/clases incluidos).

**Renovación de token (refresh):** el access token expira (30 min) y se entrega un refresh de 7 días (`POST /auth/refresh` válido solo con refresh). El interceptor renueva el access **antes** de que expire (margen de 60s) y, si llega un 401, reintenta una vez con el token nuevo; solo si el refresh también falla hace logout y redirige a `/login`.

---

## 3. DOCKER / INFRAESTRUCTURA (qué decir)

**Persistencia y orden de arranque:**
- MySQL monta el volumen `mysql_data` en `/var/lib/mysql`: los datos **sobreviven al `docker-compose down`**; solo se pierden si borro el volumen con `-v`.
- Uso **healthcheck** (mysqladmin ping) y `depends_on: condition: service_healthy`, así el backend arranca solo cuando MySQL está realmente listo, evitando conexiones rechazadas.

**Red interna:**
- Los 3 servicios se comunican por **nombre de servicio** (no por IP): `DATABASE_URL` usa `@mysql:3306` y el proxy usa `http://backend:5000`. Compose crea una red interna por defecto.

**¿Por qué `--host=0.0.0.0`?**
- Por defecto Flask escucha solo en 127.0.0.1 dentro del contenedor, inaccesible desde fuera y por el frontend; `0.0.0.0` escucha en todas las interfaces para que el mapeo de puertos y el proxy funcionen.

**¿Por qué usuario no-root?**
- Por **mínimo privilegio** / hardening: por defecto Docker corre como root; si el proceso se compromete, un usuario dedicado (uid 1000) limita el daño. Instalo dependencias como root y corro la app como no-root.

---

## 4. DECISIONES DE DISEÑO (a defender)

**Backend — separación routes / controllers / models:**
- **Routes**: solo exponen el endpoint HTTP, sin lógica de negocio (blueprints).
- **Controllers**: reglas del dominio, validaciones, autorización y orquestación.
- **Models**: mapeo ORM (clase = tabla, atributo = columna) + `to_dict()` sin exponer campos sensibles.
- **Decorators** (rol_requerido): autorización transversal reutilizada en todas las rutas sin repetir código (DRY).

**Beneficios que defiendo:**
- **Testeabilidad**: cada capa se testea aislada (mock del controller o la BD).
- **Mantenibilidad**: agrego un módulo creando blueprint + controller + models sin tocar el resto.
- **Desacoplamiento**: la lógica no depende de Flask ni del driver; cambiar de MySQL a PostgreSQL es solo cambiar el URI (requisito obligatorio cumplido).
- **DRY**: el control de roles vive en un único lugar y se reutiliza.

**Frontend — separación views / components / stores / services / routes:**
- **views** = páginas completas; **components** = piezas de UI reutilizables con props.
- **stores** (Pinia) = estado global de sesión (token + usuario) sin pasarlo por props.
- **services** = encapsulan Axios e interceptores en un solo punto (adjuntar token, manejar 401).
- **routes** = rutas + navigation guards para protección en frontend.
- **Modularidad con Blueprints**: cada dominio (auth, usuarios, cursos, inscripciones) con su prefijo de URL; módulos y clases van anidados bajo cursos.

---

## 5. LAS 5 PREGUNTAS (máximo 2 oraciones c/u)

**P1 — ¿Por qué Blueprints y por qué separar routes de controllers?**
> Los Blueprints modularizan la app por dominio, cada uno con su prefijo de URL. Separar la capa HTTP de la lógica y del acceso a datos aplica responsabilidad única y deja el motor de BD desacoplado: si cambio MySQL por PostgreSQL, solo cambio el URI.

**P2 — ¿Cómo garantizas que una ruta solo la use quien corresponde?**
> Con doble capa: en backend, `@jwt_required()` valida el token y `rol_requerido()` verifica el rol del usuario devolviendo 403 si no corresponde; en frontend, el Navigation Guard protege las rutas. Es defensa en profundidad: el frontend solo oculta la UI, la autorización real siempre se decide en el servidor.

**P3 — ¿Dónde está la persistencia y qué pasa con `docker-compose down`?**
> Los datos viven en el volumen `mysql_data` montado en MySQL, así que sobreviven al `down` y solo se pierden si elimino el volumen con `-v`. Además uso `depends_on` con healthcheck para que el backend arranque recién cuando MySQL esté listo.

**P4 — ¿Cómo se autentica cada request y qué pasa cuando el token expira?**
> El login devuelve un JWT firmado con la secret key (id como identidad y rol en los claims), más un refresh token; cada petición viaja con `Authorization: Bearer <token>` gracias al interceptor de Axios. Al expirar, el interceptor renueva el access con el refresh antes de reintentar la petición; si el refresh también falla, hace logout y redirige a `/login`.

**P5 — ¿Por qué `--host=0.0.0.0` y un usuario no-root?**
> El servidor por defecto escucha solo en 127.0.0.1 dentro del contenedor, inaccesible desde fuera; `0.0.0.0` lo hace escuchar en todas las interfaces para que el mapeo de puertos y el proxy funcionen. El usuario no-root aplica mínimo privilegio: si el proceso se compromete no corre como root, lo que limita el daño y es la práctica de hardening recomendada.

---

## NOTAS / ADVERTENCIAS RÁPIDAS

- **PostgreSQL vs MySQL**: el readme pide PostgreSQL pero el proyecto usa MySQL 8.0; acláralo ante el profesor o proponé el cambio (con SQLAlchemy es solo el URI).
- **Migraciones**: el esquema se crea con `db.create_all()` al iniciar (no uso Flask-Migrate). La carpeta de migraciones vacía se eliminó para dejar el repo liviano.
- **Novedades del proyecto**: se sumó el refresh token (`POST /auth/refresh`), el CRUD completo de módulos/clases y el panel de administración de usuarios en `/admin/usuarios`.
