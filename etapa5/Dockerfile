FROM python:3.12-slim

WORKDIR /app

# Copiamos requirements primero — así Docker cachea la capa de dependencias
# Si solo cambiás main.py, no reinstala todo
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY main.py .

# Uvicorn corre la app en el puerto 8000 dentro del contenedor
# --host 0.0.0.0 permite conexiones desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
