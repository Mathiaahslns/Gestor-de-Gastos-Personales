import random
import json
from datetime import datetime, timedelta
from pathlib import Path

print("🚀 Iniciando el Inyector de Datos Falsos 2.0 (Realista)...")

ruta_base = Path(__file__).parent.resolve()
archivo_config = ruta_base / "config.json"

if archivo_config.exists():
    try:
        with open(archivo_config, "r", encoding="utf-8") as f:
            config = json.load(f)
            ruta_datos = config.get("ruta_datos", str(ruta_base))
            ruta_base = Path(ruta_datos)
    except Exception:
        pass

archivo_gastos = ruta_base / "gastos.txt"

if archivo_gastos.exists():
    respaldo = ruta_base / "gastos_respaldo.txt"
    archivo_gastos.rename(respaldo)
    print(f"✅ Se guardaron tus datos reales en: {respaldo.name}")

# Diccionario inteligente: Categoría -> Lista de [Descripción, Precio Mínimo, Precio Máximo]
bd_compras = {
    "Comida": [
        ("Combo pollo Tarragona", 4500, 7500),
        ("Salida a Della Vita Cafe", 12000, 22000),
        ("Supermercado Jumbo", 35000, 85000),
        ("Empanadas/Comida rápida", 3000, 8000)
    ],
    "Juegos": [
        ("Juego en Steam", 2500, 25000),
        ("Juego PS5", 15000, 45000),
        ("Microtransacción", 1000, 5000)
    ],
    "Transporte": [
        ("Carga Bip!", 5000, 10000),
        ("Uber/Didi", 4500, 12000),
        ("Bencina JAC", 15000, 35000),
        ("Pasaje bus de acercamiento", 2000, 5000)
    ],
    "Servicios": [
        ("Spotify Premium", 6200, 6200),
        ("ChatGPT Plus", 19500, 20500), # Varía un poco por el dólar
        ("Cuenta de luz", 18000, 28000),
        ("Plan celular", 9990, 14990)
    ],
    "Hogar": [
        ("Artículos de aseo", 8000, 20000),
        ("Repuesto de ferretería", 2500, 15000),
        ("Cosas para la casa", 5000, 25000)
    ],
    "Otros": [
        ("Entrada partido Colo-Colo", 8000, 15000),
        ("Ropa en Tricot", 12000, 35000),
        ("Gasto hormiga / Kiosko", 1000, 4000)
    ]
}

ingreso_falso = 850000
gastos_generados = []
hoy = datetime.now()

print("🎲 Generando historial de 4 meses con precios lógicos...")

for _ in range(65):
    dias_restar = random.randint(0, 120)
    fecha_gasto = (hoy - timedelta(days=dias_restar))
    
    # Selecciona una categoría al azar
    cat_elegida = random.choice(list(bd_compras.keys()))
    
    # Selecciona un gasto realista dentro de esa categoría
    desc, min_val, max_val = random.choice(bd_compras[cat_elegida])
    
    # Genera un precio aleatorio en ese rango, redondeado a la centena más cercana (ej: 4600)
    monto_crudo = random.randint(min_val, max_val)
    monto_final = round(monto_crudo / 100) * 100
    
    gastos_generados.append({
        "fecha": fecha_gasto.strftime("%Y-%m-%d"),
        "linea": f"{fecha_gasto.strftime('%Y-%m-%d')}|{monto_final}|{cat_elegida}|{desc}|"
    })

gastos_generados.sort(key=lambda x: x["fecha"])

with open(archivo_gastos, "w", encoding="utf-8") as f:
    f.write(f"{ingreso_falso}\n")
    for g in gastos_generados:
        f.write(g["linea"] + "\n")

print(f"🔥 ¡Tiquitaca! 65 movimientos hiper-realistas listos en {archivo_gastos.name}.")