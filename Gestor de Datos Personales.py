from pathlib import Path
from datetime import datetime

CARPETA_SCRIPT = Path(__file__).parent.resolve()
ARCHIVO = CARPETA_SCRIPT / "gastos.txt"

CATEGORIAS = ["Comida", "Juegos", "Transporte", "Servicios", "Hogar", "Otros"]

def cargar_datos():
    ingreso = 0
    gastos = []

    if ARCHIVO.exists():
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            if lineas:
                try: 
                    ingreso = int(lineas[0].strip())

                    for linea in lineas[1:]:
                        partes = linea.strip().split("|")
                        if len(partes) == 4:
                            gastos.append({
                                "fecha": partes[0],
                                "monto": int(partes[1]),
                                "categoria": partes[2],
                                "descripcion": partes[3]
                            })
                except ValueError:
                    print("Error al leer el archivo. Se leerá desde cero.")

    return ingreso, gastos

def guardar_datos(ingreso, gastos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        archivo.write(f"{ingreso}\n")

        for gasto in gastos:
            archivo.write(f"{gasto['fecha']}|{gasto['monto']}|{gasto['categoria']}|{gasto['descripcion']}\n")

def pedir_numero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        entrada = entrada.replace(".", "")

        try:
            valor = int(entrada)
            if valor <= 0:
                print("¡OJO! El monto tiene que ser mayor a cero.")
            else:
                return valor
        except ValueError:
            print("¡ERROR! Tienes que ingresar un numero valido (ej: 15000). Intentalo de nuevo.")

def obtener_gastos_del_mes(gastos):
    mes_actual = datetime.now().strftime("%Y-%m")
    gastos_mes = [g for g in gastos if g["fecha"].startswith(mes_actual)]
    return gastos_mes

def registrar_gasto(gastos):
    print("\n--- REGISTRAR NUEVO GASTO ---")
    monto = pedir_numero("Ingresa el monto del gasto (ej: 15000): ")

    print("Elige la categoría del gasto")
    for i, categoria in enumerate(CATEGORIAS, 1):
        print(f" {i}. {categoria}")

    while True:
        try:
            opcion_cat = int(input("Ingresa el número de la categoría: "))
            if 1 <= opcion_cat <= len(CATEGORIAS):
                categoria_elegida = CATEGORIAS[opcion_cat - 1]
                break
            else:
                print("Opción inválida. Elige un número de la lista.")
        except ValueError:
            print("Por favor ingresa un número.")

    descripcion = input("Ingresa una breve descripción del gasto (ej: Completos en el Doggis): ")

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    gastos.append({
        "fecha": fecha_hoy,
        "monto": monto,
        "categoria": categoria_elegida,
        "descripcion": descripcion
    })
    print("Gasto registrado")

def mostrar_resumen(ingreso, gastos):
    print("\n--- RESUMEN MENSUAL ---")

    gastos_mes = obtener_gastos_del_mes(gastos)
    total_gastado = sum(gasto["monto"] for gasto in gastos_mes)
    plata_restante = ingreso - total_gastado

    print(f"Presupuesto mensual: ${ingreso:,}".replace(",", "."))
    print(f"Gastado este mes:    ${total_gastado:,}".replace(",", "."))
    print(f"Plata restante:      ${plata_restante:,}".replace(",", "."))

    if plata_restante <= 0:
        print(f"\n¡ALERTA ROJA! Te quedaste sin plata (o estas en saldo negativo).")
    elif plata_restante < (ingreso * 0.2):
        print(f"\n¡Cuidado! Te queda menos del 20% del presupuesto. Ojo con los gastos hormiga")

def mostrar_historial(gastos):
    print("\n--- HISTORIAL DE GASTOS ---")
    gastos_mes = obtener_gastos_del_mes(gastos)

    if not gastos_mes:
        print("Todavia no hay gastos registrados. ¡Buena esa, puro ahorro!")
    else:
        for i, gasto in enumerate(gastos_mes, 1):
            monto_formateado = f"{gasto['monto']:,}".replace(",", ".")
            print(f"{i}. [{gasto['fecha']}] {gasto['categoria']}: ${monto_formateado} - {gasto['descripcion']}")

def main():
    print("¡Bienvenido a tu Gestor de Datos Personales")

    ingreso, gastos = cargar_datos()

    if ingreso == 0:
        print(f"\nParece que es tu primera vez por acá (no existe el archivo 'gastos.txt')")
        ingreso = pedir_numero("Para empezar, ingresa tu presupuesto/ingreso mensual: ")
        guardar_datos(ingreso, gastos)

    while True:
        print("\n" + "="*30)
        print("         MENÚ PRINCIPAL")
        print("="*30)
        print("1. Registrar un nuevo gasto")
        print("2. Mostrar resumen del presupuesto")
        print("3. Mostrar historial detallado")
        print("4. Salir")

        try:
            opcion = int(input("\nElige una opción (1-4): ").strip())
        except ValueError:
            print("Opción no válida. Ingresa un número")
            continue

        if opcion == 1:
            registrar_gasto(gastos)
            guardar_datos(ingreso, gastos)
        elif opcion == 2:
            mostrar_resumen(ingreso, gastos)
        elif opcion == 3:
            mostrar_historial(gastos)
        elif opcion == 4:
            print("¡Nos vemos! Que te rinda la plata. ¡Chau!")
            break
        else:
            print("Esta opción no existe. Tiene que elegir un número entre 1 y 4.")

if __name__ == "__main__":
    main()