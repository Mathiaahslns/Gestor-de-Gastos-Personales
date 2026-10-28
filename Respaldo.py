import shutil
from pathlib import Path
from datetime import datetime

CARPETA_ORIGEN = Path(__file__).parent.resolve()

fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CARPETA_RESPALDO = CARPETA_ORIGEN / f"Respaldo_{fecha_actual}"

CARPETA_RESPALDO.mkdir(exist_ok=True)

archivos_a_respaldar = [
    "Gestor de Datos Personales.py",
    "App_Grafica.py",                
    "gastos.txt"                     
]

print(f"--- INICIANDO RESPALDO ---")
print(f"Creando copia en: {CARPETA_RESPALDO.name}\n")

for archivo in archivos_a_respaldar:
    ruta_archivo = CARPETA_ORIGEN / archivo

    if ruta_archivo.exists():
        shutil.copy2(ruta_archivo, CARPETA_RESPALDO)
        print(f"Copiado con éxito: {archivo}")
    else:
        print(f"No se encontró: {archivo} (Revisa si el nombre está bien escrito)")

print("\n¡Respaldo completado, compadre!")