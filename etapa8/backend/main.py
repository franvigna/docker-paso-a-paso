from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from datetime import date
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="API Becarios", version="4.0.0")

# CORS: permite que el frontend en localhost:5173 llame a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ["DATABASE_URL"]


class BecarioCreate(BaseModel):
    dni: str
    nombre: str
    apellido: str
    fecha_ingreso: date
    categoria: Literal["Inicial", "Intermedio", "Superior", "Líder", "Senior"]

class BecarioUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    fecha_ingreso: date | None = None
    categoria: Literal["Inicial", "Intermedio", "Superior", "Líder", "Senior"] | None = None


def get_connection():
    return psycopg2.connect(DATABASE_URL)

def becario_o_404(cur, id: int):
    cur.execute("SELECT * FROM becarios WHERE id = %s", (id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Becario con id {id} no encontrado")
    return dict(row)


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
    campos = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            becario_o_404(cur, id)
            set_clause = ", ".join(f"{k} = %({k})s" for k in campos)
            campos["id"] = id
            cur.execute(f"UPDATE becarios SET {set_clause} WHERE id = %(id)s RETURNING *", campos)
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
