# Imagen base: Python 3.12 en su versión liviana
FROM python:3.12-slim

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos nuestro script al contenedor
# COPY <origen en tu maquina> <destino en el contenedor>
COPY script.py .

# Comando que se ejecuta cuando el contenedor arranca
CMD ["python", "script.py"]
