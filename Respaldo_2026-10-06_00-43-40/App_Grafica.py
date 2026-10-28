import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime

CARPETA_SCRIPT = Path(__file__).parent.resolve()
ARCHIVO = CARPETA_SCRIPT / "gastos.txt"
CATEGORIAS = ["Comida", "Juegos", "Transporte", "Servicios", "Hogar", "Otros"]

ingreso_actual = 0
gastos_actuales = []

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
                    pass
    return ingreso, gastos

def guardar_datos(ingreso, gastos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        archivo.write(f"{ingreso}\n")
        for gasto in gastos:
            archivo.write(f"{gasto['fecha']}|{gasto['monto']}|{gasto['categoria']}|{gasto['descripcion']}\n")

def obtener_gastos_del_mes(gastos):
    mes_actual = datetime.now().strftime("%Y-%m")
    gastos_mes = [g for g in gastos if g["fecha"].startswith(mes_actual)]
    return gastos_mes

def verificar_primera_vez():
    """Esta función se ejecuta apenas abre la ventana para pedir la plata inicial"""
    global ingreso_actual, gastos_actuales
    ingreso_actual, gastos_actuales = cargar_datos()

    if ingreso_actual == 0:
        dialog = ctk.CTkInputDialog(text="¡Bienvenido! Ingresa tu presupuesto mensual (ej: 300.000):", title="Configurar Presupuesto")
        entrada = dialog.get_input()
        
        if entrada:
            entrada = entrada.replace(".", "")
            try:
                ingreso_actual = int(entrada)
                if ingreso_actual <= 0:
                    messagebox.showwarning("Error", "El presupuesto debe ser mayor a cero. Vuelve a abrir el programa.")
                    app.destroy() # Cierra la app
                    return
                guardar_datos(ingreso_actual, gastos_actuales)
            except ValueError:
                messagebox.showwarning("Error", "Debes ingresar un número. Vuelve a abrir el programa.")
                app.destroy()
                return
        else:
            app.destroy() 
            return

    actualizar_pantalla()

def actualizar_pantalla():
    """Calcula y dibuja el resumen y el historial en la caja de texto"""
    gastos_mes = obtener_gastos_del_mes(gastos_actuales)
    total_gastado = sum(g["monto"] for g in gastos_mes)
    plata_restante = ingreso_actual - total_gastado

    texto = "💰 RESUMEN DEL MES\n"
    texto += "-" * 30 + "\n"
    texto += f"Presupuesto: ${ingreso_actual:,}\n".replace(",", ".")
    texto += f"Gastado:     ${total_gastado:,}\n".replace(",", ".")
    texto += f"Restante:    ${plata_restante:,}\n\n".replace(",", ".")

    if plata_restante <= 0:
        texto += "🚨 ¡ALERTA ROJA! Te quedaste sin plata.\n\n"
    elif plata_restante < (ingreso_actual * 0.2):
        texto += "⚠️ ¡Cuidado! Te queda menos del 20% del presupuesto.\n\n"

    texto += "📋 HISTORIAL DE GASTOS\n"
    texto += "-" * 30 + "\n"
    
    if not gastos_mes:
        texto += "Todavía no hay gastos registrados este mes. ¡Puro ahorro!\n"
    else:
        for i, gasto in enumerate(gastos_mes, 1):
            monto_fmt = f"{gasto['monto']:,}".replace(",", ".")
            texto += f"{i}. [{gasto['fecha']}] {gasto['categoria']}: ${monto_fmt} - {gasto['descripcion']}\n"

    texto_historial.configure(state="normal")
    texto_historial.delete("0.0", "end")
    texto_historial.insert("0.0", texto)
    texto_historial.configure(state="disabled")

def guardar_gasto_gui():
    """Toma lo que el usuario escribió y lo guarda"""
    monto_str = entrada_monto.get().strip().replace(".", "")
    categoria = combo_categoria.get()
    descripcion = entrada_desc.get().strip()

    try:
        monto = int(monto_str)
        if monto <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Cuidado", "Ingresa un monto válido mayor a cero.")
        return

    if categoria not in CATEGORIAS:
        messagebox.showwarning("Cuidado", "Por favor elige una categoría.")
        return

    if not descripcion:
        descripcion = "Sin descripción"

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    gastos_actuales.append({
        "fecha": fecha_hoy,
        "monto": monto,
        "categoria": categoria,
        "descripcion": descripcion
    })
    
    guardar_datos(ingreso_actual, gastos_actuales)
    actualizar_pantalla()

    entrada_monto.delete(0, "end")
    entrada_desc.delete(0, "end")
    combo_categoria.set("Categoría")
    
    messagebox.showinfo("Éxito", "¡Gasto registrado al toque!")

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

app = ctk.CTk()
app.geometry("800x500")
app.title("Gestor de Gastos Personales")

frame_izquierdo = ctk.CTkFrame(app)
frame_izquierdo.pack(side="left", fill="both", expand=True, padx=20, pady=20)

frame_derecho = ctk.CTkFrame(app)
frame_derecho.pack(side="right", fill="both", expand=True, padx=20, pady=20)

titulo_form = ctk.CTkLabel(frame_izquierdo, text="Registrar Gasto", font=("Arial", 20, "bold"))
titulo_form.pack(pady=20)

entrada_monto = ctk.CTkEntry(frame_izquierdo, placeholder_text="Monto (ej: 15.000)")
entrada_monto.pack(pady=10, padx=20, fill="x")

combo_categoria = ctk.CTkComboBox(frame_izquierdo, values=CATEGORIAS)
combo_categoria.pack(pady=10, padx=20, fill="x")
combo_categoria.set("Categoría")

entrada_desc = ctk.CTkEntry(frame_izquierdo, placeholder_text="Descripción del gasto")
entrada_desc.pack(pady=10, padx=20, fill="x")

btn_guardar = ctk.CTkButton(frame_izquierdo, text="Guardar Gasto", command=guardar_gasto_gui, font=("Arial", 14, "bold"))
btn_guardar.pack(pady=30)

titulo_resumen = ctk.CTkLabel(frame_derecho, text="Estado de Cuenta", font=("Arial", 20, "bold"))
titulo_resumen.pack(pady=10)

texto_historial = ctk.CTkTextbox(frame_derecho, state="disabled", font=("Courier", 13))
texto_historial.pack(fill="both", expand=True, padx=20, pady=10)

app.after(100, verificar_primera_vez)

app.mainloop()