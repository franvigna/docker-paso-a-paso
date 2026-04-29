# CRUD Becarios — Stack Local con Docker

Aplicación full-stack para gestionar becarios, orquestada con Docker Compose.

## Stack

| Servicio      | Tecnología                | Puerto |
|---------------|---------------------------|--------|
| Frontend      | React + TypeScript + Vite | 5173   |
| Backend       | Python + FastAPI          | 8000   |
| Base de datos | PostgreSQL 16             | 5432   |

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop)

Nada más. No necesitás instalar Python, Node ni PostgreSQL.

## Levantar el proyecto

```bash
docker compose up --build
```

La primera vez tarda unos minutos en descargar las imágenes base.

## URLs

| URL                          | Descripción                     |
|------------------------------|---------------------------------|
| http://localhost:5173        | Frontend                        |
| http://localhost:8000/docs   | API — documentación interactiva |
| http://localhost:8000/health | API — health check              |

## Apagar

```bash
# Apagar (los datos persisten)
docker compose down

# Apagar y borrar todos los datos
docker compose down -v
```

## Modelo de datos

| Campo         | Tipo   | Valores permitidos                           |
|---------------|--------|----------------------------------------------|
| dni           | string | único                                        |
| nombre        | string | —                                            |
| apellido      | string | —                                            |
| fecha_ingreso | date   | —                                            |
| categoria     | string | Inicial, Intermedio, Superior, Líder, Senior |

## Estructura

```
etapa9/
├── docker-compose.yml
├── backend/
│   ├── main.py           # API REST con FastAPI
│   ├── init.sql          # Crea la tabla al primer arranque
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── App.tsx
    │   ├── main.tsx
    │   ├── types.ts
    │   └── components/
    │       ├── BecariosList.tsx
    │       └── BecarioForm.tsx
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    ├── package.json
    └── Dockerfile
```
