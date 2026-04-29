from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from datetime import date
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="API Becarios - CRUD Completo", version="3.0.0")

DATABASE_URL = os.environ["DATABASE_URL"]


# --- Modelos Pydantic ---

class BecarioCreate(BaseModel):
    """Datos requeridos para crear un becario. FastAPI valida esto automáticamente."""
    dni: str
    nombre: str
    apellido: str
    fecha_ingreso: date
    categoria: Literal["Inicial", "Intermedio", "Superior", "Líder", "Senior"]

class BecarioUpdate(BaseModel):
    """Todos los campos son opcionales para permitir actualizaciones parciales."""
    nombre: str | None = None
    apellido: str | None = None
    fecha_ingreso: date | None = None
    categoria: Literal["Inicial", "Intermedio", "Superior", "Líder", "Senior"] | None = None


# --- Helpers ---

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def becario_o_404(cur, id: int):
    """Busca un becario por id y lanza 404 si no existe."""
    cur.execute("SELECT * FROM becarios WHERE id = %s", (id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Becario con id {id} no encontrado")
    return dict(row)


# --- Endpoints ---

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/becarios")
def listar_becarios():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM becarios ORDER BY id")
            return list(cur.fetchall())
    finally:
        conn.close()


@app.get("/becarios/{id}")
def obtener_becario(id: int):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            return becario_o_404(cur, id)
    finally:
        conn.close()


@app.post("/becarios", status_code=201)
def crear_becario(becario: BecarioCreate):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO becarios (dni, nombre, apellido, fecha_ingreso, categoria)
                VALUES (%(dni)s, %(nombre)s, %(apellido)s, %(fecha_ingreso)s, %(categoria)s)
                RETURNING *
                """,
                becario.model_dump()
            )
            nuevo = cur.fetchone()
        conn.commit()
        return dict(nuevo)
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Ya existe un becario con ese DNI")
    finally:
        conn.close()


@app.put("/becarios/{id}")
def actualizar_becario(id: int, datos: BecarioUpdate):
    # Filtramos solo los campos que el cliente envió (no None)
    campos = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            becario_o_404(cur, id)
            # Construimos el SET dinámicamente con los campos recibidos
            set_clause = ", ".join(f"{k} = %({k})s" for k in campos)
            campos["id"] = id
            cur.execute(
                f"UPDATE becarios SET {set_clause} WHERE id = %(id)s RETURNING *",
                campos
            )
            actualizado = cur.fetchone()
        conn.commit()
        return dict(actualizado)
    finally:
        conn.close()


@app.delete("/becarios/{id}", status_code=204)
def eliminar_becario(id: int):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            becario_o_404(cur, id)
            cur.execute("DELETE FROM becarios WHERE id = %s", (id,))
        conn.commit()
    finally:
        conn.close()
