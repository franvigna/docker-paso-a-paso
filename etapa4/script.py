# Script simple para demostrar Python corriendo dentro de un contenedor

import sys
import platform

print("Hola desde Python dentro de Docker!")
print(f"Versión de Python: {sys.version}")
print(f"Sistema operativo del contenedor: {platform.system()} {platform.release()}")
