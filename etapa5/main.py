# FastAPI es el framework para construir la API
from fastapi import FastAPI

# Creamos la instancia de la aplicación
app = FastAPI(title="API Becarios", version="1.0.0")

# Definimos un endpoint: GET /health
# El decorador @app.get indica que este endpoint responde a requests GET en la ruta /health
@app.get("/health")
def health_check():
    # FastAPI convierte automáticamente el dict a JSON
    return {"status": "ok"}
