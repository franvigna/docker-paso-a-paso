from fastapi import FastAPI, HTTPException
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="API Becarios", version="2.0.0")

# Leemos la URL de conexión desde una variable de entorno
DATABASE_URL = os.environ["DATABASE_URL"]

def get_connection():
    """Abre y devuelve una conexión a la base de datos."""
    return psycopg2.connect(DATABASE_URL)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/becarios")
def listar_becarios():
    """Devuelve todos los becarios de la base de datos."""
    conn = get_connection()
    try:
        # RealDictCursor hace que cada fila sea un dict en vez de una tupla
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM becarios ORDER BY id")
            becarios = cur.fetchall()
        return list(becarios)
    finally:
        conn.close()


@app.post("/becarios", status_code=201)
def crear_becario(becario: dict):
    """Inserta un nuevo becario en la base de datos."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO becarios (dni, nombre, apellido, fecha_ingreso, categoria)
                VALUES (%(dni)s, %(nombre)s, %(apellido)s, %(fecha_ingreso)s, %(categoria)s)
                RETURNING *
                """,
                becario
            )
            # RETURNING * devuelve la fila recién insertada (con el id generado)
            nuevo = cur.fetchone()
        conn.commit()
        return dict(nuevo)
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Ya existe un becario con ese DNI")
    finally:
        conn.close()
