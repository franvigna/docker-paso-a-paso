# Docker Paso a Paso

Guía práctica para aprender Docker desde cero, con ejemplos progresivos que van desde un contenedor simple hasta una aplicación full-stack lista para producción.

## ¿Qué vas a aprender?

Cada etapa agrega conceptos nuevos sobre la anterior, siguiendo una progresión lógica:

| Etapa | Tema | Tecnologías |
|-------|------|-------------|
| [etapa1](#etapa-1--instalación) | Instalación del entorno | Docker Desktop, WSL2, VS Code |
| [etapa2](./etapa2) | Docker Compose + servidor web estático | Nginx |
| [etapa3](./etapa3) | Base de datos como servicio | PostgreSQL |
| [etapa4](./etapa4) | Construcción de imágenes personalizadas | Python, Dockerfile |
| [etapa5](./etapa5) | API web en contenedor con live reload | FastAPI, Uvicorn |
| [etapa6](./etapa6) | API conectada a base de datos | FastAPI + PostgreSQL |
| [etapa7](./etapa7) | CRUD completo con validación | FastAPI, Pydantic |
| [etapa8](./etapa8) | Frontend + Backend + Base de datos | React, FastAPI, PostgreSQL |
| [etapa9](./etapa9) | Healthchecks y buenas prácticas | Docker Compose avanzado |

## Requisitos

Solo necesitás tener instalado **Docker Desktop**.

## Cómo usar este repositorio

Cada etapa es independiente. Entrá a la carpeta de la etapa que quieras explorar y levantá los servicios:

```bash
cd etapaN
docker compose up --build
```

Para detener:

```bash
docker compose down
```

Para detener y eliminar los volúmenes (datos):

```bash
docker compose down -v
```

## Detalle de cada etapa

### Etapa 1 — Instalación

Antes de arrancar necesitás tener el entorno listo. Instalá las siguientes herramientas:

- **Docker Desktop** — motor de contenedores con interfaz gráfica
  - Windows/Mac: [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)
  - En Windows también instala automáticamente **WSL2** (subsistema Linux), que Docker necesita para funcionar

- **Visual Studio Code** — editor recomendado
  - [code.visualstudio.com](https://code.visualstudio.com/)
  - Extensión recomendada: **Docker** (de Microsoft) — te permite ver contenedores, imágenes y volúmenes desde el editor

Verificá que todo funcione abriendo una terminal y ejecutando:

```bash
docker --version
docker compose version
```

Si ambos comandos devuelven una versión, estás listo para empezar.

---

### Etapa 2 — Servidor web con Nginx
Primer contacto con Docker Compose. Levanta un Nginx que sirve una página HTML estática desde un volumen local.
- URL: http://localhost:8080

### Etapa 3 — Base de datos PostgreSQL
Servicio de base de datos con persistencia mediante volúmenes nombrados.
- Puerto: `localhost:5432`

### Etapa 4 — Imagen personalizada con Python
Construcción de una imagen propia con Dockerfile. Un script Python muestra información del entorno dentro del contenedor.

### Etapa 5 — API con FastAPI
Servicio web Python con FastAPI y Uvicorn, orquestado con Docker Compose e incluye live reload para desarrollo.
- URL: http://localhost:8000

### Etapa 6 — API + Base de datos
La API se conecta a PostgreSQL. Implementa dos endpoints para gestionar becarios con operaciones de lectura y escritura.
- API: http://localhost:8000
- Endpoints: `GET /becarios`, `POST /becarios`

### Etapa 7 — CRUD completo
CRUD completo con validación de datos usando Pydantic, manejo de errores HTTP y actualizaciones parciales.
- API: http://localhost:8000
- Endpoints: `GET /becarios`, `GET /becarios/{id}`, `POST /becarios`, `PUT /becarios/{id}`, `DELETE /becarios/{id}`

### Etapa 8 — Full-Stack con React
Tres servicios orquestados: frontend React (TypeScript + Vite), backend FastAPI y PostgreSQL. Incluye CORS y comunicación entre servicios.
- Frontend: http://localhost:5173
- API: http://localhost:8000

### Etapa 9 — Healthchecks y producción
Agrega healthchecks a la base de datos para que el backend espere a que PostgreSQL esté realmente listo antes de arrancar.
- Frontend: http://localhost:5173
- API: http://localhost:8000
