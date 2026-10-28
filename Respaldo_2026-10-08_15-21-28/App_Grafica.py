import sys
import json
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- 1. RUTAS Y CONFIGURACIÓN PERSISTENTE ---
if getattr(sys, 'frozen', False):
    CARPETA_BASE = Path(sys.executable).parent.resolve()
else:
    CARPETA_BASE = Path(__file__).parent.resolve()

ARCHIVO_CONFIG = CARPETA_BASE / "config.json"

# Configuración por defecto
CONFIG = {
    "tema": "Oscuro",
    "zoom": "100%",
    "moneda": "$",
    "idioma": "es",
    "alertas": True,
    "ruta_datos": str(CARPETA_BASE)
}

def cargar_config():
    global CONFIG
    if ARCHIVO_CONFIG.exists():
        try:
            with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
                CONFIG.update(json.load(f))
        except Exception:
            pass
    aplicar_tema_zoom_inicial()

def guardar_config():
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=4)

def aplicar_tema_zoom_inicial():
    ctk.set_appearance_mode("dark" if CONFIG["tema"] == "Oscuro" else "light")
    escala = float(CONFIG["zoom"].replace("%", "")) / 100
    ctk.set_widget_scaling(escala)
    ctk.set_window_scaling(escala)

def obtener_ruta_archivo():
    return Path(CONFIG["ruta_datos"]) / "gastos.txt"


# --- 2. SISTEMA DE IDIOMAS ---
# --- 2. SISTEMA DE IDIOMAS ---
TEXTOS = {
    "es": {
        "titulo": "Gestor de Gastos Personales", "reg_gasto": "Registrar Gasto", "ph_monto": "Monto (ej: 15000)", "ph_desc": "Descripción del gasto", "btn_guardar": "Guardar Gasto", "btn_borrar": "Borrar un Gasto", "btn_ajustes": "Ajustes", "btn_reset": "Reset Total", "dash_ingresos": "Ingresos:", "dash_gastos": "Gastos:", "dash_disp": "Disponible:", "dash_pct": "Gastas el {}% de tus ingresos", "tit_movs": "Últimos Movimientos", "sin_movs": "Aún no hay movimientos registrados en este mes.\n", "cat_comida": "Comida", "cat_juegos": "Juegos", "cat_transporte": "Transporte", "cat_servicios": "Servicios", "cat_hogar": "Hogar", "cat_otros": "Otros", "aj_zoom": "Zoom Visual", "aj_tema": "Apariencia", "aj_idioma": "Idioma / Language", "aj_moneda": "Moneda", "aj_alertas": "Alertas Emergentes", "aj_ruta": "Ruta de Base de Datos", "aj_info": "Información", "aj_peligro": "Peligro", "sw_alertas": "Activar ventanas de error/éxito", "btn_cambiar_ruta": "Cambiar Carpeta", "btn_acerca": "Acerca de...", "btn_restaurar": "Restaurar Ajustes por Defecto", "alerta_cuidado": "Cuidado", "alerta_monto": "Ingresa un monto válido mayor a cero.", "alerta_listo": "Listo", "alerta_borrado": "El gasto fue eliminado exitosamente.", "lbl_sel_borrar": "Selecciona el gasto que quieres borrar:", "alerta_peligro": "¡Peligro!", "alerta_reset": "¿Borrar TODO tu historial?"
    },
    "en": {
        "titulo": "Personal Expense Manager", "reg_gasto": "Register Expense", "ph_monto": "Amount (e.g., 15000)", "ph_desc": "Expense description", "btn_guardar": "Save Expense", "btn_borrar": "Delete an Expense", "btn_ajustes": "Settings", "btn_reset": "Total Reset", "dash_ingresos": "Income:", "dash_gastos": "Expenses:", "dash_disp": "Available:", "dash_pct": "You spend {}% of your income", "tit_movs": "Latest Movements", "sin_movs": "No movements recorded this month yet.\n", "cat_comida": "Food", "cat_juegos": "Gaming", "cat_transporte": "Transport", "cat_servicios": "Services", "cat_hogar": "Home", "cat_otros": "Other", "aj_zoom": "Visual Zoom", "aj_tema": "Appearance", "aj_idioma": "Language", "aj_moneda": "Currency", "aj_alertas": "Pop-up Alerts", "aj_ruta": "Database Path", "aj_info": "Information", "aj_peligro": "Danger", "sw_alertas": "Enable success/error pop-ups", "btn_cambiar_ruta": "Change Folder", "btn_acerca": "About...", "btn_restaurar": "Restore Default Settings", "alerta_cuidado": "Warning", "alerta_monto": "Enter a valid amount greater than zero.", "alerta_listo": "Done", "alerta_borrado": "Expense successfully deleted.", "lbl_sel_borrar": "Select the expense you want to delete:", "alerta_peligro": "Danger!", "alerta_reset": "Delete ALL your history?"
    },
    "pt": {
        "titulo": "Gestor de Despesas", "reg_gasto": "Registrar Despesa", "ph_monto": "Valor (ex: 15000)", "ph_desc": "Descrição da despesa", "btn_guardar": "Salvar Despesa", "btn_borrar": "Apagar Despesa", "btn_ajustes": "Configurações", "btn_reset": "Reset Total", "dash_ingresos": "Receitas:", "dash_gastos": "Despesas:", "dash_disp": "Disponível:", "dash_pct": "Você gasta {}% da sua receita", "tit_movs": "Últimos Movimentos", "sin_movs": "Ainda não há movimentos neste mês.\n", "cat_comida": "Alimentação", "cat_juegos": "Jogos", "cat_transporte": "Transporte", "cat_servicios": "Serviços", "cat_hogar": "Casa", "cat_otros": "Outros", "aj_zoom": "Zoom Visual", "aj_tema": "Aparência", "aj_idioma": "Idioma", "aj_moneda": "Moeda", "aj_alertas": "Alertas Pop-up", "aj_ruta": "Caminho dos Dados", "aj_info": "Informação", "aj_peligro": "Perigo", "sw_alertas": "Ativar janelas de erro/sucesso", "btn_cambiar_ruta": "Mudar Pasta", "btn_acerca": "Sobre...", "btn_restaurar": "Restaurar Padrões", "alerta_cuidado": "Atenção", "alerta_monto": "Insira um valor maior que zero.", "alerta_listo": "Pronto", "alerta_borrado": "Despesa apagada com sucesso.", "lbl_sel_borrar": "Selecione a despesa para apagar:", "alerta_peligro": "Perigo!", "alerta_reset": "Apagar TODO o seu histórico?"
    },
    "fr": {
        "titulo": "Gestionnaire de Dépenses", "reg_gasto": "Enregistrer Dépense", "ph_monto": "Montant (ex: 15000)", "ph_desc": "Description de la dépense", "btn_guardar": "Sauvegarder", "btn_borrar": "Supprimer Dépense", "btn_ajustes": "Paramètres", "btn_reset": "Réinitialisation", "dash_ingresos": "Revenus:", "dash_gastos": "Dépenses:", "dash_disp": "Disponible:", "dash_pct": "Vous dépensez {}% de vos revenus", "tit_movs": "Derniers Mouvements", "sin_movs": "Aucun mouvement enregistré ce mois-ci.\n", "cat_comida": "Nourriture", "cat_juegos": "Jeux", "cat_transporte": "Transport", "cat_servicios": "Services", "cat_hogar": "Maison", "cat_otros": "Autres", "aj_zoom": "Zoom Visuel", "aj_tema": "Apparence", "aj_idioma": "Langue", "aj_moneda": "Devise", "aj_alertas": "Alertes Pop-up", "aj_ruta": "Chemin des Données", "aj_info": "Information", "aj_peligro": "Danger", "sw_alertas": "Activer les alertes", "btn_cambiar_ruta": "Changer Dossier", "btn_acerca": "À propos...", "btn_restaurar": "Restaurer les Paramètres", "alerta_cuidado": "Attention", "alerta_monto": "Entrez un montant supérieur à zéro.", "alerta_listo": "Terminé", "alerta_borrado": "Dépense supprimée avec succès.", "lbl_sel_borrar": "Sélectionnez la dépense à supprimer:", "alerta_peligro": "Danger!", "alerta_reset": "Supprimer TOUT votre historique?"
    },
    "it": {
        "titulo": "Gestore di Spese", "reg_gasto": "Registra Spesa", "ph_monto": "Importo (es: 15000)", "ph_desc": "Descrizione della spesa", "btn_guardar": "Salva Spesa", "btn_borrar": "Elimina Spesa", "btn_ajustes": "Impostazioni", "btn_reset": "Reset Totale", "dash_ingresos": "Entrate:", "dash_gastos": "Spese:", "dash_disp": "Disponibile:", "dash_pct": "Spendi il {}% delle tue entrate", "tit_movs": "Ultimi Movimenti", "sin_movs": "Nessun movimento registrato questo mese.\n", "cat_comida": "Cibo", "cat_juegos": "Giochi", "cat_transporte": "Trasporto", "cat_servicios": "Servizi", "cat_hogar": "Casa", "cat_otros": "Altro", "aj_zoom": "Zoom Visivo", "aj_tema": "Aspetto", "aj_idioma": "Lingua", "aj_moneda": "Valuta", "aj_alertas": "Avvisi Pop-up", "aj_ruta": "Percorso Dati", "aj_info": "Informazioni", "aj_peligro": "Pericolo", "sw_alertas": "Abilita avvisi", "btn_cambiar_ruta": "Cambia Cartella", "btn_acerca": "Info su...", "btn_restaurar": "Ripristina Impostazioni", "alerta_cuidado": "Attenzione", "alerta_monto": "Inserisci un importo maggiore di zero.", "alerta_listo": "Fatto", "alerta_borrado": "Spesa eliminata con successo.", "lbl_sel_borrar": "Seleziona la spesa da eliminare:", "alerta_peligro": "Pericolo!", "alerta_reset": "Eliminare TUTTO il tuo storico?"
    },
    "de": {
        "titulo": "Ausgabenmanager", "reg_gasto": "Ausgabe Registrieren", "ph_monto": "Betrag (z.B. 15000)", "ph_desc": "Beschreibung der Ausgabe", "btn_guardar": "Speichern", "btn_borrar": "Ausgabe Löschen", "btn_ajustes": "Einstellungen", "btn_reset": "Vollständiger Reset", "dash_ingresos": "Einnahmen:", "dash_gastos": "Ausgaben:", "dash_disp": "Verfügbar:", "dash_pct": "Sie geben {}% Ihres Einkommens aus", "tit_movs": "Letzte Bewegungen", "sin_movs": "Diesen Monat noch keine Bewegungen.\n", "cat_comida": "Essen", "cat_juegos": "Spiele", "cat_transporte": "Transport", "cat_servicios": "Dienste", "cat_hogar": "Haus", "cat_otros": "Sonstiges", "aj_zoom": "Visueller Zoom", "aj_tema": "Erscheinungsbild", "aj_idioma": "Sprache", "aj_moneda": "Währung", "aj_alertas": "Pop-up Warnungen", "aj_ruta": "Datenbankpfad", "aj_info": "Information", "aj_peligro": "Gefahr", "sw_alertas": "Warnungen aktivieren", "btn_cambiar_ruta": "Ordner Ändern", "btn_acerca": "Über...", "btn_restaurar": "Standard Wiederherstellen", "alerta_cuidado": "Achtung", "alerta_monto": "Geben Sie einen Betrag größer als null ein.", "alerta_listo": "Fertig", "alerta_borrado": "Ausgabe erfolgreich gelöscht.", "lbl_sel_borrar": "Wählen Sie die zu löschende Ausgabe:", "alerta_peligro": "Gefahr!", "alerta_reset": "GESAMTEN Verlauf löschen?"
    }
}

MESES = {
    "es": {"01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril", "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto", "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"},
    "en": {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"},
    "pt": {"01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril", "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto", "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"},
    "fr": {"01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril", "05": "Mai", "06": "Juin", "07": "Juillet", "08": "Août", "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Décembre"},
    "it": {"01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile", "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto", "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"},
    "de": {"01": "Januar", "02": "Februar", "03": "März", "04": "April", "05": "Mai", "06": "Juni", "07": "Juli", "08": "August", "09": "September", "10": "Oktober", "11": "November", "12": "Dezember"}
}

def t(clave):
    return TEXTOS[CONFIG["idioma"]].get(clave, clave)

def mostrar_alerta(tipo, titulo, mensaje):
    if CONFIG["alertas"]:
        if tipo == "info": messagebox.showinfo(titulo, mensaje)
        elif tipo == "warning": messagebox.showwarning(titulo, mensaje)
        elif tipo == "error": messagebox.showerror(titulo, mensaje)


# --- 3. BACKEND DE DATOS ---
ingreso_actual = 0
gastos_actuales = []
widget_grafico = None
pantalla_completa = False

def cargar_datos():
    ingreso = 0
    gastos = []
    archivo = obtener_ruta_archivo()
    if archivo.exists():
        with open(archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
            if lineas:
                try: 
                    ingreso = int(lineas[0].strip())
                    for linea in lineas[1:]:
                        partes = linea.strip().split("|")
                        if len(partes) == 4:
                            gastos.append({"fecha": partes[0], "monto": int(partes[1]), "categoria": partes[2], "descripcion": partes[3]})
                except ValueError:
                    pass
    return ingreso, gastos

def guardar_datos(ingreso, gastos):
    archivo = obtener_ruta_archivo()
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(f"{ingreso}\n")
        for gasto in gastos:
            f.write(f"{gasto['fecha']}|{gasto['monto']}|{gasto['categoria']}|{gasto['descripcion']}\n")

def obtener_meses_disponibles():
    meses = set(gasto["fecha"][:7] for gasto in gastos_actuales)
    meses.add(datetime.now().strftime("%Y-%m"))
    return sorted(list(meses), reverse=True)

def obtener_gastos_del_mes(mes_seleccionado):
    return [g for g in gastos_actuales if g["fecha"].startswith(mes_seleccionado)]


# --- 4. INTERFAZ Y ACTUALIZACIONES ---
def aplicar_textos_ui():
    app.title(t("titulo"))
    titulo_form.configure(text=t("reg_gasto"))
    entrada_monto.configure(placeholder_text=t("ph_monto"))
    entrada_desc.configure(placeholder_text=t("ph_desc"))
    btn_guardar.configure(text=t("btn_guardar"))
    btn_eliminar.configure(text=t("btn_borrar"))
    btn_ajustes.configure(text=t("btn_ajustes"))
    btn_reset.configure(text=t("btn_reset"))
    lbl_titulo_historial.configure(text=t("tit_movs"))
    
    categorias_loc = [t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")]
    combo_categoria.configure(values=categorias_loc)
    combo_categoria.set(categorias_loc[0])
    
    actualizar_pantalla()

def dibujar_grafico(gastos_mes):
    global widget_grafico
    if widget_grafico is not None:
        widget_grafico.destroy()
    if not gastos_mes:
        return 

    totales_por_categoria = {}
    for gasto in gastos_mes:
        cat = gasto["categoria"]
        totales_por_categoria[cat] = totales_por_categoria.get(cat, 0) + gasto["monto"]

    totales_ordenados = sorted(totales_por_categoria.items(), key=lambda x: x[1])

    etiquetas = []
    valores = []
    for cat, monto in totales_ordenados:
        # Buscamos la clave original (ej: "cat_comida") que corresponde a tu categoría (ej: "Comida")
        clave_real = next((k for k, v in TEXTOS["es"].items() if v == cat), cat)
        
        # Traducimos usando esa clave limpia
        etiquetas.append(t(clave_real))
        valores.append(monto)

    color_fondo = '#2B2B2B' if CONFIG["tema"] == "Oscuro" else '#EBEBEB'
    color_texto = 'white' if CONFIG["tema"] == "Oscuro" else 'black'
    color_barra = '#3498DB' # Un azul moderno para las barras

    fig, ax = plt.subplots(figsize=(4, 2.5), facecolor=color_fondo)

    # Crear las barras horizontales
    barras = ax.barh(etiquetas, valores, color=color_barra, height=0.6)

    # Limpiar el diseño para que se vea mas minimalista (sin bordes ni ejes molestos)
    ax.set_facecolor(color_fondo)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_visible(False) # Ocultar la regla de números de abajo
    ax.tick_params(axis='y', colors=color_texto, length=0, labelsize=10) # Letras de las categorías

    # Agregar los montos exactos de texto al final de cada barra
    mon = CONFIG["moneda"]
    for barra in barras:
        ancho = barra.get_width()
        texto_monto = f" {mon}{int(ancho):,}".replace(",", ".")
        ax.text(ancho, barra.get_y() + barra.get_height()/2, texto_monto, 
                va='center', ha='left', color=color_texto, fontweight='bold', fontsize=10)

    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    widget_grafico = canvas.get_tk_widget()
    widget_grafico.pack(fill="both", expand=True)

def actualizar_pantalla(*args):
    mes_seleccionado = combo_meses.get()
    if not mes_seleccionado or mes_seleccionado == "Cargando...": return
    
    gastos_mes = obtener_gastos_del_mes(mes_seleccionado)
    total_gastado = sum(g["monto"] for g in gastos_mes)
    plata_restante = ingreso_actual - total_gastado
    pct_gasto = (total_gastado / ingreso_actual) * 100 if ingreso_actual > 0 else 0

    anio, mes_num = mes_seleccionado.split("-")
    nombre_mes = MESES[CONFIG["idioma"]].get(mes_num, mes_num)
    lbl_dash_mes.configure(text=f"{nombre_mes} {anio}")
    
    mon = CONFIG["moneda"]
    lbl_dash_ingresos.configure(text=f"{t('dash_ingresos')} {mon}{ingreso_actual:,}".replace(",", "."))
    lbl_dash_gastos.configure(text=f"{t('dash_gastos')} {mon}{total_gastado:,}".replace(",", "."))
    lbl_dash_disponible.configure(text=f"{t('dash_disp')} {mon}{plata_restante:,}".replace(",", "."))
    lbl_dash_porcentaje.configure(text=t("dash_pct").format(f"{pct_gasto:.1f}".replace(".", ",")))

    color_normal = "white" if CONFIG["tema"] == "Oscuro" else "black"
    if plata_restante <= 0:
        lbl_dash_disponible.configure(text_color="#E74C3C") 
        lbl_dash_porcentaje.configure(text_color="#E74C3C")
    elif plata_restante < (ingreso_actual * 0.2):
        lbl_dash_disponible.configure(text_color="#F39C12") 
        lbl_dash_porcentaje.configure(text_color="#F39C12")
    else:
        lbl_dash_disponible.configure(text_color=color_normal)
        lbl_dash_porcentaje.configure(text_color=color_normal)

    texto = ""
    if not gastos_mes:
        texto += t("sin_movs")
    else:
        for i, gasto in enumerate(gastos_mes, 1):
            monto_fmt = f"{gasto['monto']:,}".replace(",", ".")
            texto += f"[{gasto['fecha']}] {gasto['categoria']}: {mon}{monto_fmt} - {gasto['descripcion']}\n"

    texto_historial.configure(state="normal")
    texto_historial.delete("0.0", "end")
    texto_historial.insert("0.0", texto)
    texto_historial.configure(state="disabled")
    dibujar_grafico(gastos_mes)

def verificar_primera_vez():
    global ingreso_actual, gastos_actuales
    ingreso_actual, gastos_actuales = cargar_datos()

    if ingreso_actual == 0:
        dialog = ctk.CTkInputDialog(text=f"Ingresa tu presupuesto / Enter budget:", title="Presupuesto Inicial")
        entrada = dialog.get_input()
        if entrada:
            entrada = entrada.replace(".", "")
            try:
                ingreso_actual = int(entrada)
                if ingreso_actual <= 0:
                    app.destroy()
                    return
                guardar_datos(ingreso_actual, gastos_actuales)
            except ValueError:
                app.destroy()
                return
        else:
            app.destroy()
            return

    combo_meses.configure(values=obtener_meses_disponibles())
    combo_meses.set(datetime.now().strftime("%Y-%m"))
    aplicar_textos_ui()

def guardar_gasto_gui():
    monto_str = entrada_monto.get().strip().replace(".", "")
    categoria = combo_categoria.get()
    descripcion = entrada_desc.get().strip()

    try:
        monto = int(monto_str)
        if monto <= 0: raise ValueError
    except ValueError:
        mostrar_alerta("warning", t("alerta_cuidado"), t("alerta_monto"))
        return

    if not descripcion: descripcion = "..."

    gastos_actuales.append({
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "monto": monto,
        "categoria": categoria, 
        "descripcion": descripcion
    })
    
    guardar_datos(ingreso_actual, gastos_actuales)
    combo_meses.configure(values=obtener_meses_disponibles())
    combo_meses.set(datetime.now().strftime("%Y-%m"))
    actualizar_pantalla()

    entrada_monto.delete(0, "end")
    entrada_desc.delete(0, "end")

def abrir_ajustes():
    ventana_ajustes = ctk.CTkToplevel(app)
    ventana_ajustes.title(t("btn_ajustes"))
    ventana_ajustes.geometry("450x650") # Un pelito más de altura para que respire
    ventana_ajustes.attributes("-topmost", True)

    scroll = ctk.CTkScrollableFrame(ventana_ajustes)
    scroll.pack(fill="both", expand=True, padx=10, pady=10)

    # Le damos nombre a los Labels para poder actualizarlos después
    lbl_titulo_ajustes = ctk.CTkLabel(scroll, text=t("btn_ajustes"), font=("Arial", 20, "bold"))
    lbl_titulo_ajustes.pack(pady=10)

    # 1. Zoom
    lbl_zoom = ctk.CTkLabel(scroll, text=t("aj_zoom"), font=("Arial", 12, "bold"))
    lbl_zoom.pack(pady=(10, 0))
    def set_zoom(valor):
        CONFIG["zoom"] = valor
        escala = float(valor.replace("%", "")) / 100
        ctk.set_widget_scaling(escala)
        ctk.set_window_scaling(escala)
        guardar_config()
        
    seg_zoom = ctk.CTkSegmentedButton(scroll, values=["80%", "100%", "125%", "150%"], command=set_zoom)
    seg_zoom.set(CONFIG["zoom"])
    seg_zoom.pack(pady=5, fill="x", padx=20)

    # 2. Modo (Tema)
    lbl_tema = ctk.CTkLabel(scroll, text=t("aj_tema"), font=("Arial", 12, "bold"))
    lbl_tema.pack(pady=(15, 0))
    def set_tema(valor):
        tema_interno = "Oscuro" if valor in ["Oscuro", "Dark"] else "Claro"
        CONFIG["tema"] = tema_interno
        ctk.set_appearance_mode("dark" if tema_interno == "Oscuro" else "light")
        guardar_config()
        actualizar_pantalla() 
        
    opciones_tema = ["Claro", "Oscuro"] if CONFIG["idioma"] == "es" else ["Light", "Dark"]
    seg_tema = ctk.CTkSegmentedButton(scroll, values=opciones_tema, command=set_tema)
    seg_tema.set(opciones_tema[1] if CONFIG["tema"] == "Oscuro" else opciones_tema[0])
    seg_tema.pack(pady=5, fill="x", padx=20)

    # 3. Idioma
    lbl_idioma = ctk.CTkLabel(scroll, text=t("aj_idioma"), font=("Arial", 12, "bold"))
    lbl_idioma.pack(pady=(15, 0))
    
    mapa_idiomas = {
        "Español": "es", "English": "en", "Português": "pt", 
        "Français": "fr", "Italiano": "it", "Deutsch": "de"
    }
    mapa_inverso = {v: k for k, v in mapa_idiomas.items()}

    def set_idioma(valor):
        CONFIG["idioma"] = mapa_idiomas[valor]
        guardar_config()
        aplicar_textos_ui() # Refresca la app de fondo
        actualizar_textos_ajustes() # <--- ¡LA MAGIA NUEVA AQUÍ! Refresca esta misma ventana
        
    opt_idioma = ctk.CTkOptionMenu(scroll, values=list(mapa_idiomas.keys()), command=set_idioma)
    opt_idioma.set(mapa_inverso.get(CONFIG["idioma"], "Español"))
    opt_idioma.pack(pady=5, fill="x", padx=20)

    # 4. Moneda
    lbl_moneda = ctk.CTkLabel(scroll, text=t("aj_moneda"), font=("Arial", 12, "bold"))
    lbl_moneda.pack(pady=(15, 0))
    def set_moneda(valor):
        CONFIG["moneda"] = valor
        guardar_config()
        actualizar_pantalla()
        
    seg_moneda = ctk.CTkSegmentedButton(scroll, values=["$", "US$", "€", "£"], command=set_moneda)
    seg_moneda.set(CONFIG["moneda"] if CONFIG["moneda"] in ["$", "US$", "€", "£"] else "$")
    seg_moneda.pack(pady=5, fill="x", padx=20)

    # 5. Alertas
    lbl_alertas = ctk.CTkLabel(scroll, text=t("aj_alertas"), font=("Arial", 12, "bold"))
    lbl_alertas.pack(pady=(15, 0))
    def toggle_alertas():
        CONFIG["alertas"] = switch_alertas.get() == 1
        guardar_config()
        
    switch_alertas = ctk.CTkSwitch(scroll, text=t("sw_alertas"), command=toggle_alertas)
    if CONFIG["alertas"]: switch_alertas.select()
    switch_alertas.pack(pady=5)

    # 6. Carpeta de Datos
    lbl_ruta_tit = ctk.CTkLabel(scroll, text=t("aj_ruta"), font=("Arial", 12, "bold"))
    lbl_ruta_tit.pack(pady=(15, 0))
    lbl_ruta = ctk.CTkLabel(scroll, text=CONFIG["ruta_datos"], text_color="gray", font=("Arial", 10))
    lbl_ruta.pack()
    
    def cambiar_ruta():
        nueva_ruta = filedialog.askdirectory(title=t("btn_cambiar_ruta"))
        if nueva_ruta:
            ruta_antigua = obtener_ruta_archivo()
            CONFIG["ruta_datos"] = nueva_ruta
            ruta_nueva = obtener_ruta_archivo()
            if ruta_antigua.exists() and str(ruta_antigua) != str(ruta_nueva):
                shutil.move(str(ruta_antigua), str(ruta_nueva))
            lbl_ruta.configure(text=nueva_ruta)
            guardar_config()
            mostrar_alerta("info", t("alerta_listo"), "Ruta actualizada.")
            
    btn_ruta = ctk.CTkButton(scroll, text=t("btn_cambiar_ruta"), fg_color="#3498DB", hover_color="#2980B9", command=cambiar_ruta)
    btn_ruta.pack(pady=5)

    # 7. Acerca de
    lbl_info = ctk.CTkLabel(scroll, text=t("aj_info"), font=("Arial", 12, "bold"))
    lbl_info.pack(pady=(25, 0))
    def mostrar_acerca_de():
        texto_about = f"{t('titulo')} V4.0\n\nDev: Mathias\nIngeniería Civil Informática\nUniversidad de Valparaíso"
        mostrar_alerta("info", t("btn_acerca"), texto_about)
        
    btn_about = ctk.CTkButton(scroll, text=t("btn_acerca"), fg_color="#27AE60", hover_color="#1E8449", command=mostrar_acerca_de)
    btn_about.pack(pady=5, fill="x", padx=20)

    # 8. Restaurar
    lbl_peligro = ctk.CTkLabel(scroll, text=t("aj_peligro"), font=("Arial", 12, "bold"))
    lbl_peligro.pack(pady=(25, 0))
    def restaurar_fabrica():
        resp = messagebox.askyesno(t("aj_peligro"), "¿Volver a la configuración predeterminada?")
        if resp:
            if ARCHIVO_CONFIG.exists(): ARCHIVO_CONFIG.unlink()
            mostrar_alerta("info", "Reinicio / Restart", "Cierra y vuelve a abrir el programa.")
            ventana_ajustes.destroy()
            
    btn_rest = ctk.CTkButton(scroll, text=t("btn_restaurar"), fg_color="#C0392B", hover_color="#922B21", command=restaurar_fabrica)
    btn_rest.pack(pady=5, fill="x", padx=20)

    # 9. Botón Guardar / Cerrar
    textos_guardar = {
        "es": "Guardar Cambios", "en": "Save Changes", "pt": "Salvar Alterações",
        "fr": "Enregistrer", "it": "Salva Modifiche", "de": "Speichern"
    }
    
    def guardar_y_cerrar():
        guardar_config() 
        ventana_ajustes.destroy() 

    btn_guardar_ajustes = ctk.CTkButton(
        ventana_ajustes, 
        text=textos_guardar.get(CONFIG["idioma"], "Guardar Cambios"),
        fg_color="#27AE60", hover_color="#1E8449", font=("Arial", 14, "bold"),
        height=40, command=guardar_y_cerrar
    )
    btn_guardar_ajustes.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    # --- FUNCIÓN PARA REFRESCAR TEXTOS EN VIVO DENTRO DE LOS AJUSTES ---
    def actualizar_textos_ajustes():
        ventana_ajustes.title(t("btn_ajustes"))
        lbl_titulo_ajustes.configure(text=t("btn_ajustes"))
        lbl_zoom.configure(text=t("aj_zoom"))
        lbl_tema.configure(text=t("aj_tema"))
        
        # Traducir los botones de "Claro/Oscuro" a "Light/Dark" en vivo
        opciones_tema_nuevas = ["Claro", "Oscuro"] if CONFIG["idioma"] == "es" else ["Light", "Dark"]
        seg_tema.configure(values=opciones_tema_nuevas)
        seg_tema.set(opciones_tema_nuevas[1] if CONFIG["tema"] == "Oscuro" else opciones_tema_nuevas[0])

        lbl_idioma.configure(text=t("aj_idioma"))
        lbl_moneda.configure(text=t("aj_moneda"))
        lbl_alertas.configure(text=t("aj_alertas"))
        switch_alertas.configure(text=t("sw_alertas"))
        lbl_ruta_tit.configure(text=t("aj_ruta"))
        btn_ruta.configure(text=t("btn_cambiar_ruta"))
        lbl_info.configure(text=t("aj_info"))
        btn_about.configure(text=t("btn_acerca"))
        lbl_peligro.configure(text=t("aj_peligro"))
        btn_rest.configure(text=t("btn_restaurar"))
        btn_guardar_ajustes.configure(text=textos_guardar.get(CONFIG["idioma"], "Guardar Cambios"))

def abrir_ventana_eliminar():
    mes_actual = combo_meses.get()
    gastos_mes = obtener_gastos_del_mes(mes_actual)

    if not gastos_mes:
        mostrar_alerta("warning", "Aviso", "No hay gastos en este mes para eliminar.")
        return

    ventana_eliminar = ctk.CTkToplevel(app)
    ventana_eliminar.title(t("btn_borrar"))
    ventana_eliminar.geometry("500x200")
    ventana_eliminar.attributes("-topmost", True)

    opciones = []
    for g in gastos_mes:
        idx_real = gastos_actuales.index(g)
        monto_fmt = f"{g['monto']:,}".replace(",", ".")
        mon = CONFIG["moneda"]
        opciones.append(f"{idx_real} | [{g['fecha']}] {g['categoria']} - {mon}{monto_fmt}")

    lbl_info = ctk.CTkLabel(ventana_eliminar, text=t("lbl_sel_borrar"), font=("Arial", 14))
    lbl_info.pack(pady=15)

    combo_borrar = ctk.CTkComboBox(ventana_eliminar, values=opciones, width=400)
    combo_borrar.pack(pady=5)
    combo_borrar.set(opciones[0])

    def confirmar_borrado():
        seleccion = combo_borrar.get()
        idx_real = int(seleccion.split(" | ")[0])
        
        del gastos_actuales[idx_real] 
        guardar_datos(ingreso_actual, gastos_actuales) 
        actualizar_pantalla()
        ventana_eliminar.destroy()
        mostrar_alerta("info", t("alerta_listo"), t("alerta_borrado"))

    btn_confirmar = ctk.CTkButton(ventana_eliminar, text=t("btn_borrar"), fg_color="#C0392B", hover_color="#922B21", command=confirmar_borrado)
    btn_confirmar.pack(pady=15)

def resetear_datos_gui():
    if messagebox.askyesno(t("alerta_peligro"), t("alerta_reset")):
        if obtener_ruta_archivo().exists(): obtener_ruta_archivo().unlink() 
        app.destroy()


# --- 5. ARRANQUE PRINCIPAL ---
cargar_config()

app = ctk.CTk()  
app.geometry("950x700")

frame_izquierdo = ctk.CTkFrame(app, width=300)
frame_izquierdo.pack(side="left", fill="y", expand=False, padx=(20, 10), pady=20)

frame_derecho = ctk.CTkFrame(app)
frame_derecho.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

# PANEL IZQUIERDO
titulo_form = ctk.CTkLabel(frame_izquierdo, text="", font=("Arial", 20, "bold"))
titulo_form.pack(pady=20)

entrada_monto = ctk.CTkEntry(frame_izquierdo)
entrada_monto.pack(pady=10, padx=20, fill="x")

combo_categoria = ctk.CTkComboBox(frame_izquierdo, values=[])
combo_categoria.pack(pady=10, padx=20, fill="x")

entrada_desc = ctk.CTkEntry(frame_izquierdo)
entrada_desc.pack(pady=10, padx=20, fill="x")

btn_guardar = ctk.CTkButton(frame_izquierdo, text="", command=guardar_gasto_gui, font=("Arial", 14, "bold"))
btn_guardar.pack(pady=(20, 10), padx=20, fill="x")

btn_eliminar = ctk.CTkButton(frame_izquierdo, text="", command=abrir_ventana_eliminar, fg_color="#E67E22", hover_color="#D35400", font=("Arial", 12, "bold"))
btn_eliminar.pack(pady=5, padx=20, fill="x")

frame_inferior = ctk.CTkFrame(frame_izquierdo, fg_color="transparent")
frame_inferior.pack(side="bottom", fill="x", padx=20, pady=20)

btn_ajustes = ctk.CTkButton(frame_inferior, text="", command=abrir_ajustes)
btn_ajustes.pack(pady=5, fill="x")

btn_reset = ctk.CTkButton(frame_inferior, text="", command=resetear_datos_gui, fg_color="#C0392B", hover_color="#922B21")
btn_reset.pack(pady=5, fill="x")

# PANEL DERECHO
combo_meses = ctk.CTkComboBox(frame_derecho, values=["Cargando..."], command=actualizar_pantalla)
combo_meses.pack(pady=(20, 5), padx=20, fill="x")

lbl_dash_mes = ctk.CTkLabel(frame_derecho, text="Mes", font=("Arial", 28, "bold"))
lbl_dash_mes.pack(pady=(0, 10))

frame_dashboard = ctk.CTkFrame(frame_derecho, fg_color="transparent")
frame_dashboard.pack(fill="x", padx=20, pady=5)

frame_stats = ctk.CTkFrame(frame_dashboard, fg_color="transparent")
frame_stats.pack(side="left", fill="both", expand=True)

lbl_dash_ingresos = ctk.CTkLabel(frame_stats, text="", font=("Arial", 17))
lbl_dash_ingresos.pack(anchor="w", pady=5)
lbl_dash_gastos = ctk.CTkLabel(frame_stats, text="", font=("Arial", 17))
lbl_dash_gastos.pack(anchor="w", pady=5)
lbl_dash_disponible = ctk.CTkLabel(frame_stats, text="", font=("Arial", 20, "bold"))
lbl_dash_disponible.pack(anchor="w", pady=5)
lbl_dash_porcentaje = ctk.CTkLabel(frame_stats, text="", font=("Arial", 16))
lbl_dash_porcentaje.pack(anchor="w", pady=5)

frame_grafico = ctk.CTkFrame(frame_dashboard, fg_color="transparent")
frame_grafico.pack(side="right", fill="both", expand=True)

lbl_titulo_historial = ctk.CTkLabel(frame_derecho, text="", font=("Arial", 16, "bold"))
lbl_titulo_historial.pack(anchor="w", padx=20, pady=(20, 5))

texto_historial = ctk.CTkTextbox(frame_derecho, state="disabled", font=("Courier", 14), height=180)
texto_historial.pack(fill="both", expand=True, padx=20, pady=(0, 20))

app.after(100, verificar_primera_vez)
app.mainloop()