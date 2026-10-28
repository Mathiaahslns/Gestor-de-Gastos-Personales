import sys
import json
import shutil
import tkinter as tk    
import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime, timedelta

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
    import json # Solo por si no estaba importado arriba
    try:
        # Nota: si tu archivo de ajustes tiene otro nombre (ej: "ajustes.json"), cámbialo en la línea de abajo.
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(CONFIG, f, indent=4)
    except Exception as e:
        print("Pifia guardando la memoria compadre:", e)

def aplicar_tema_zoom_inicial():
    ctk.set_appearance_mode("dark" if CONFIG["tema"] == "Oscuro" else "light")
    escala = float(CONFIG["zoom"].replace("%", "")) / 100
    ctk.set_widget_scaling(escala)
    ctk.set_window_scaling(escala)

def obtener_ruta_archivo():
    return Path(CONFIG["ruta_datos"]) / "gastos.txt"

# --- 2. SISTEMA DE IDIOMAS ---
TEXTOS = {
    "es": {
        "titulo": "Gestor de Gastos Personales", "reg_gasto": "Registrar Gasto", "ph_monto": "Monto (ej: 15000)", "ph_desc": "Descripción del gasto", "btn_guardar": "Guardar Gasto", "btn_reset": "Reset Total", "dash_ingresos": "Ingresos:", "dash_gastos": "Gastos:", "dash_disp": "Disponible:", "dash_pct": "Gastas el {}% de tus ingresos", "tit_movs": "Últimos Movimientos", "sin_movs": "Aún no hay movimientos registrados en este mes.\n", "cat_comida": "Comida", "cat_juegos": "Juegos", "cat_transporte": "Transporte", "cat_servicios": "Servicios", "cat_hogar": "Hogar", "cat_otros": "Otros", "aj_zoom": "Zoom Visual", "aj_tema": "Apariencia", "aj_idioma": "Idioma / Language", "aj_moneda": "Moneda", "aj_alertas": "Alertas Emergentes", "aj_ruta": "Ruta de Base de Datos", "aj_info": "Información", "aj_peligro": "Peligro", "sw_alertas": "Activar ventanas de error/éxito", "btn_cambiar_ruta": "Cambiar Carpeta", "btn_acerca": "Acerca de...", "btn_restaurar": "Restaurar Ajustes por Defecto", "alerta_cuidado": "Cuidado", "alerta_monto": "Ingresa un monto válido mayor a cero.", "alerta_listo": "Listo", "alerta_borrado": "El gasto fue eliminado exitosamente.", "lbl_sel_borrar": "Selecciona el gasto que quieres borrar:", "alerta_peligro": "¡Peligro!", "alerta_reset": "¿Borrar TODO tu historial?"
    },
    "en": {
        "titulo": "Personal Expense Manager", "reg_gasto": "Register Expense", "ph_monto": "Amount (e.g., 15000)", "ph_desc": "Expense description", "btn_guardar": "Save Expense", "btn_reset": "Total Reset", "dash_ingresos": "Income:", "dash_gastos": "Expenses:", "dash_disp": "Available:", "dash_pct": "You spend {}% of your income", "tit_movs": "Latest Movements", "sin_movs": "No movements recorded this month yet.\n", "cat_comida": "Food", "cat_juegos": "Gaming", "cat_transporte": "Transport", "cat_servicios": "Services", "cat_hogar": "Home", "cat_otros": "Other", "aj_zoom": "Visual Zoom", "aj_tema": "Appearance", "aj_idioma": "Language", "aj_moneda": "Currency", "aj_alertas": "Pop-up Alerts", "aj_ruta": "Database Path", "aj_info": "Information", "aj_peligro": "Danger", "sw_alertas": "Enable success/error pop-ups", "btn_cambiar_ruta": "Change Folder", "btn_acerca": "About...", "btn_restaurar": "Restore Default Settings", "alerta_cuidado": "Warning", "alerta_monto": "Enter a valid amount greater than zero.", "alerta_listo": "Done", "alerta_borrado": "Expense successfully deleted.", "lbl_sel_borrar": "Select the expense you want to delete:", "alerta_peligro": "Danger!", "alerta_reset": "Delete ALL your history?"
    },
    "pt": {
        "titulo": "Gestor de Despesas", "reg_gasto": "Registrar Despesa", "ph_monto": "Valor (ex: 15000)", "ph_desc": "Descrição da despesa", "btn_guardar": "Salvar Despesa", "btn_reset": "Reset Total", "dash_ingresos": "Receitas:", "dash_gastos": "Despesas:", "dash_disp": "Disponível:", "dash_pct": "Você gasta {}% da sua receita", "tit_movs": "Últimos Movimentos", "sin_movs": "Ainda não há movimentos neste mês.\n", "cat_comida": "Alimentação", "cat_juegos": "Jogos", "cat_transporte": "Transporte", "cat_servicios": "Serviços", "cat_hogar": "Casa", "cat_otros": "Outros", "aj_zoom": "Zoom Visual", "aj_tema": "Aparência", "aj_idioma": "Idioma", "aj_moneda": "Moeda", "aj_alertas": "Alertas Pop-up", "aj_ruta": "Caminho dos Dados", "aj_info": "Informação", "aj_peligro": "Perigo", "sw_alertas": "Ativar janelas de erro/sucesso", "btn_cambiar_ruta": "Mudar Pasta", "btn_acerca": "Sobre...", "btn_restaurar": "Restaurar Padrões", "alerta_cuidado": "Atenção", "alerta_monto": "Insira um valor maior que zero.", "alerta_listo": "Pronto", "alerta_borrado": "Despesa apagada com sucesso.", "lbl_sel_borrar": "Selecione a despesa para apagar:", "alerta_peligro": "Perigo!", "alerta_reset": "Apagar TODO o seu histórico?"
    },
    "fr": {
        "titulo": "Gestionnaire de Dépenses", "reg_gasto": "Enregistrer Dépense", "ph_monto": "Montant (ex: 15000)", "ph_desc": "Description de la dépense", "btn_guardar": "Sauvegarder", "btn_reset": "Réinitialisation", "dash_ingresos": "Revenus:", "dash_gastos": "Dépenses:", "dash_disp": "Disponible:", "dash_pct": "Vous dépensez {}% de vos revenus", "tit_movs": "Derniers Mouvements", "sin_movs": "Aucun mouvement enregistré ce mois-ci.\n", "cat_comida": "Nourriture", "cat_juegos": "Jeux", "cat_transporte": "Transport", "cat_servicios": "Services", "cat_hogar": "Maison", "cat_otros": "Autres", "aj_zoom": "Zoom Visuel", "aj_tema": "Apparence", "aj_idioma": "Langue", "aj_moneda": "Devise", "aj_alertas": "Alertes Pop-up", "aj_ruta": "Chemin des Données", "aj_info": "Information", "aj_peligro": "Danger", "sw_alertas": "Activer les alertes", "btn_cambiar_ruta": "Changer Dossier", "btn_acerca": "À propos...", "btn_restaurar": "Restaurer les Paramètres", "alerta_cuidado": "Attention", "alerta_monto": "Entrez un montant supérieur à zéro.", "alerta_listo": "Terminé", "alerta_borrado": "Dépense supprimée avec succès.", "lbl_sel_borrar": "Sélectionnez la dépense à supprimer:", "alerta_peligro": "Danger!", "alerta_reset": "Supprimer TOUT votre historique?"
    },
    "it": {
        "titulo": "Gestore di Spese", "reg_gasto": "Registra Spesa", "ph_monto": "Importo (es: 15000)", "ph_desc": "Descrizione della spesa", "btn_guardar": "Salva Spesa",  "btn_reset": "Reset Totale", "dash_ingresos": "Entrate:", "dash_gastos": "Spese:", "dash_disp": "Disponibile:", "dash_pct": "Spendi il {}% delle tue entrate", "tit_movs": "Ultimi Movimenti", "sin_movs": "Nessun movimento registrato questo mese.\n", "cat_comida": "Cibo", "cat_juegos": "Giochi", "cat_transporte": "Trasporto", "cat_servicios": "Servizi", "cat_hogar": "Casa", "cat_otros": "Altro", "aj_zoom": "Zoom Visivo", "aj_tema": "Aspetto", "aj_idioma": "Lingua", "aj_moneda": "Valuta", "aj_alertas": "Avvisi Pop-up", "aj_ruta": "Percorso Dati", "aj_info": "Informazioni", "aj_peligro": "Pericolo", "sw_alertas": "Abilita avvisi", "btn_cambiar_ruta": "Cambia Cartella", "btn_acerca": "Info su...", "btn_restaurar": "Ripristina Impostazioni", "alerta_cuidado": "Attenzione", "alerta_monto": "Inserisci un importo maggiore di zero.", "alerta_listo": "Fatto", "alerta_borrado": "Spesa eliminata con successo.", "lbl_sel_borrar": "Seleziona la spesa da eliminare:", "alerta_peligro": "Pericolo!", "alerta_reset": "Eliminare TUTTO il tuo storico?"
    },
    "de": {
        "titulo": "Ausgabenmanager", "reg_gasto": "Ausgabe Registrieren", "ph_monto": "Betrag (z.B. 15000)", "ph_desc": "Beschreibung der Ausgabe", "btn_guardar": "Speichern", "btn_reset": "Vollständiger Reset", "dash_ingresos": "Einnahmen:", "dash_gastos": "Ausgaben:", "dash_disp": "Verfügbar:", "dash_pct": "Sie geben {}% Ihres Einkommens aus", "tit_movs": "Letzte Bewegungen", "sin_movs": "Diesen Monat noch keine Bewegungen.\n", "cat_comida": "Essen", "cat_juegos": "Spiele", "cat_transporte": "Transport", "cat_servicios": "Dienste", "cat_hogar": "Haus", "cat_otros": "Sonstiges", "aj_zoom": "Visueller Zoom", "aj_tema": "Erscheinungsbild", "aj_idioma": "Sprache", "aj_moneda": "Währung", "aj_alertas": "Pop-up Warnungen", "aj_ruta": "Datenbankpfad", "aj_info": "Information", "aj_peligro": "Gefahr", "sw_alertas": "Warnungen aktivieren", "btn_cambiar_ruta": "Ordner Ändern", "btn_acerca": "Über...", "btn_restaurar": "Standard Wiederherstellen", "alerta_cuidado": "Achtung", "alerta_monto": "Geben Sie einen Betrag größer als null ein.", "alerta_listo": "Fertig", "alerta_borrado": "Ausgabe erfolgreich gelöscht.", "lbl_sel_borrar": "Wählen Sie die zu löschende Ausgabe:", "alerta_peligro": "Gefahr!", "alerta_reset": "GESAMTEN Verlauf löschen?"
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

# --- INYECTOR DE TEXTOS PARA EL BUSCADOR ---
nuevos_textos = {
    "es": {"btn_buscar": "Buscar / Filtrar", "tit_buscar": "Explorador de Gastos", "lbl_busqueda": "Palabra clave:", "lbl_filtro_cat": "Categoría:", "lbl_filtro_mes": "Mes:", "lbl_monto_min": "Monto Min:", "lbl_orden": "Ordenar por:", "opt_todas": "Todas/Todos", "ord_fecha_desc": "Más recientes", "ord_fecha_asc": "Más antiguos", "ord_monto_desc": "Mayor monto", "ord_monto_asc": "Menor monto", "btn_aplicar_filtros": "Aplicar Filtros"},
    "en": {"btn_buscar": "Search / Filter", "tit_buscar": "Expense Explorer", "lbl_busqueda": "Keyword:", "lbl_filtro_cat": "Category:", "lbl_filtro_mes": "Month:", "lbl_monto_min": "Min Amount:", "lbl_orden": "Sort by:", "opt_todas": "All", "ord_fecha_desc": "Newest first", "ord_fecha_asc": "Oldest first", "ord_monto_desc": "Highest amount", "ord_monto_asc": "Lowest amount", "btn_aplicar_filtros": "Apply Filters"},
    "pt": {"btn_buscar": "Buscar / Filtrar", "tit_buscar": "Explorador", "lbl_busqueda": "Palavra-chave:", "lbl_filtro_cat": "Categoria:", "lbl_filtro_mes": "Mês:", "lbl_monto_min": "Valor Min:", "lbl_orden": "Ordenar por:", "opt_todas": "Todas/Todos", "ord_fecha_desc": "Mais recentes", "ord_fecha_asc": "Mais antigos", "ord_monto_desc": "Maior valor", "ord_monto_asc": "Menor valor", "btn_aplicar_filtros": "Aplicar Filtros"},
    "fr": {"btn_buscar": "Chercher / Filtrer", "tit_buscar": "Explorateur", "lbl_busqueda": "Mot-clé:", "lbl_filtro_cat": "Catégorie:", "lbl_filtro_mes": "Mois:", "lbl_monto_min": "Montant Min:", "lbl_orden": "Trier par:", "opt_todas": "Tout", "ord_fecha_desc": "Plus récents", "ord_fecha_asc": "Plus anciens", "ord_monto_desc": "Montant max", "ord_monto_asc": "Montant min", "btn_aplicar_filtros": "Appliquer Filtres"},
    "it": {"btn_buscar": "Cerca / Filtra", "tit_buscar": "Esploratore", "lbl_busqueda": "Parola chiave:", "lbl_filtro_cat": "Categoria:", "lbl_filtro_mes": "Mese:", "lbl_monto_min": "Importo Min:", "lbl_orden": "Ordina per:", "opt_todas": "Tutti", "ord_fecha_desc": "Più recenti", "ord_fecha_asc": "Più vecchi", "ord_monto_desc": "Importo mag.", "ord_monto_asc": "Importo min.", "btn_aplicar_filtros": "Applica Filtri"},
    "de": {"btn_buscar": "Suchen / Filtern", "tit_buscar": "Ausgaben-Explorer", "lbl_busqueda": "Schlüsselwort:", "lbl_filtro_cat": "Kategorie:", "lbl_filtro_mes": "Monat:", "lbl_monto_min": "Mindestbetrag:", "lbl_orden": "Sortieren nach:", "opt_todas": "Alle", "ord_fecha_desc": "Neueste zuerst", "ord_fecha_asc": "Älteste zuerst", "ord_monto_desc": "Höchster Betrag", "ord_monto_asc": "Niedrigster Betrag", "btn_aplicar_filtros": "Filter Anwenden"}
}
for lang, dic in nuevos_textos.items():
    if lang in TEXTOS:
        TEXTOS[lang].update(dic)

# --- INYECTOR 2: TEXTOS DEL SISTEMA DE MENÚ Y ALERTA ---
nuevos_textos_menu = {
    "es": {"msg_borrar": "¿Seguro que quieres borrar este gasto?", "menu_arch": "Archivo", "menu_herr": "Herramientas", "menu_ayu": "Ayuda", "menu_idi": "Idioma", "menu_salir": "Salir"},
    "en": {"msg_borrar": "Are you sure you want to delete this expense?", "menu_arch": "File", "menu_herr": "Tools", "menu_ayu": "Help", "menu_idi": "Language", "menu_salir": "Exit"},
    "pt": {"msg_borrar": "Tem certeza que deseja apagar esta despesa?", "menu_arch": "Arquivo", "menu_herr": "Ferramentas", "menu_ayu": "Ajuda", "menu_idi": "Idioma", "menu_salir": "Sair"},
    "fr": {"msg_borrar": "Êtes-vous sûr de vouloir supprimer cette dépense ?", "menu_arch": "Fichier", "menu_herr": "Outils", "menu_ayu": "Aide", "menu_idi": "Langue", "menu_salir": "Quitter"},
    "it": {"msg_borrar": "Sei sicuro di voler eliminare questa spesa?", "menu_arch": "File", "menu_herr": "Strumenti", "menu_ayu": "Aiuto", "menu_idi": "Lingua", "menu_salir": "Esci"},
    "de": {"msg_borrar": "Möchten Sie diese Ausgabe wirklich löschen?", "menu_arch": "Datei", "menu_herr": "Werkzeuge", "menu_ayu": "Hilfe", "menu_idi": "Sprache", "menu_salir": "Beenden"}
}
for lang, dic in nuevos_textos_menu.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 3: PERIODOS DE TIEMPO ---
nuevos_textos_periodos = {
    "es": {"per_hoy": "Hoy", "per_sem": "Semana", "per_mes": "Mes", "per_6m": "6 Meses", "per_ano": "Año"},
    "en": {"per_hoy": "Today", "per_sem": "Week", "per_mes": "Month", "per_6m": "6 Months", "per_ano": "Year"},
    "pt": {"per_hoy": "Hoje", "per_sem": "Semana", "per_mes": "Mês", "per_6m": "6 Meses", "per_ano": "Ano"},
    "fr": {"per_hoy": "Aujourd'hui", "per_sem": "Semaine", "per_mes": "Mois", "per_6m": "6 Mois", "per_ano": "Année"},
    "it": {"per_hoy": "Oggi", "per_sem": "Settimana", "per_mes": "Mese", "per_6m": "6 Mesi", "per_ano": "Anno"},
    "de": {"per_hoy": "Heute", "per_sem": "Woche", "per_mes": "Monat", "per_6m": "6 Monate", "per_ano": "Jahr"}
}
for lang, dic in nuevos_textos_periodos.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 4: LÍMITES POR CATEGORÍA ---
if "presupuestos_cat" not in CONFIG:
    CONFIG["presupuestos_cat"] = {} # Preparamos el espacio en la configuración

nuevos_textos_limites = {
    "es": {"btn_limites": "Límites por Categoría", "tit_limites": "Definir Presupuestos (0 = Sin Límite)", "msg_limite": "¡Alerta de Presupuesto!", "txt_superado": "¡Weón, te pasaste del límite de", "txt_guardar_igual": "¿Quieres registrar el gasto de todas formas?"},
    "en": {"btn_limites": "Category Limits", "tit_limites": "Set Budgets (0 = No Limit)", "msg_limite": "Budget Alert!", "txt_superado": "You exceeded your limit for", "txt_guardar_igual": "Do you want to save this expense anyway?"},
    "pt": {"btn_limites": "Limites por Categoria", "tit_limites": "Definir Orçamentos (0 = Sem Limite)", "msg_limite": "Alerta de Orçamento!", "txt_superado": "Você ultrapassou o limite de", "txt_guardar_igual": "Deseja registrar a despesa mesmo assim?"},
    "fr": {"btn_limites": "Limites de Catégorie", "tit_limites": "Définir Budgets (0 = Sans Limite)", "msg_limite": "Alerte Budget!", "txt_superado": "Vous avez dépassé la limite de", "txt_guardar_igual": "Voulez-vous quand même enregistrer la dépense?"},
    "it": {"btn_limites": "Limiti Categoria", "tit_limites": "Imposta Budget (0 = Nessun Limite)", "msg_limite": "Avviso Budget!", "txt_superado": "Hai superato il limite di", "txt_guardar_igual": "Vuoi registrare la spesa comunque?"},
    "de": {"btn_limites": "Kategorie-Limits", "tit_limites": "Budgets Festlegen (0 = Kein Limit)", "msg_limite": "Budget-Alarm!", "txt_superado": "Sie haben das Limit überschritten für", "txt_guardar_igual": "Möchten Sie die Ausgabe trotzdem speichern?"}
}
for lang, dic in nuevos_textos_limites.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

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
    try:
        app.title(t("titulo"))
        titulo_form.configure(text=t("reg_gasto"))
        entrada_monto.configure(placeholder_text=t("ph_monto"))
        entrada_desc.configure(placeholder_text=t("ph_desc"))
        btn_guardar.configure(text=t("btn_guardar"))
        btn_buscar.configure(text=t("btn_buscar"))
        
        # --- REPARACIÓN 1: RECARGAR LAS CATEGORÍAS ---
        categorias = [t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")]
        combo_categoria.configure(values=categorias)
        if not combo_categoria.get() or combo_categoria.get() == "CTkComboBox":
            combo_categoria.set(categorias[0])

        # --- REPARACIÓN 2: RECARGAR LA BOTONERA DE PERIODOS ---
        opciones_periodo = [t("per_hoy"), t("per_sem"), t("per_mes"), t("per_6m"), t("per_ano")]
        seg_periodos.configure(values=opciones_periodo)
        valor_actual = seg_periodos.get()
        if not valor_actual or valor_actual not in opciones_periodo or valor_actual == "CTkSegmentedButton":
            seg_periodos.set(t("per_mes"))
            
        # Actualizamos el dashboard para que el título quite el "CTKSEGMENTEDBUTTON"
        actualizar_pantalla()
        
    except Exception as e:
        print(f"Pifia menor en la interfaz ignorada: {e}")

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

def obtener_gastos_por_periodo():
    try:
        periodo_sel = seg_periodos.get()
    except:
        periodo_sel = t("per_mes") # Por defecto si aún no carga
        
    hoy = datetime.now()
    gastos_filtrados = []
    
    for g in gastos_actuales:
        try:
            fecha_g = datetime.strptime(g["fecha"], "%Y-%m-%d")
        except: continue
            
        if periodo_sel == t("per_hoy") and fecha_g.date() == hoy.date():
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_sem") and (hoy - fecha_g).days <= 7:
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_mes") and fecha_g.month == hoy.month and fecha_g.year == hoy.year:
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_6m") and (hoy - fecha_g).days <= 180:
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_ano") and fecha_g.year == hoy.year:
            gastos_filtrados.append(g)
            
    return gastos_filtrados

def actualizar_pantalla(*args):
    gastos_mes = obtener_gastos_por_periodo()
    
    periodo_texto = seg_periodos.get().upper() if seg_periodos.get() else "RESUMEN"
    lbl_dash_mes.configure(text=f"{periodo_texto}")
    total_gastado = sum(g["monto"] for g in gastos_mes)
    plata_restante = ingreso_actual - total_gastado
    pct_gasto = (total_gastado / ingreso_actual) * 100 if ingreso_actual > 0 else 0

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
    global ingreso_actual
    hoy = datetime.now()
    dia_pago = CONFIG.get("dia_pago", 1)
    
    # --- CÁLCULO DEL CICLO FINANCIERO ---
    # Si hoy es mayor o igual a tu día de pago, ya estamos en el mes actual.
    # Si no, significa que sigues gastando la plata del mes pasado.
    if hoy.day >= dia_pago:
        ciclo_actual = f"{hoy.year}-{hoy.month:02d}"
    else:
        mes_ant = hoy.month - 1 if hoy.month > 1 else 12
        anio_ant = hoy.year if hoy.month > 1 else hoy.year - 1
        ciclo_actual = f"{anio_ant}-{mes_ant:02d}"
        
    ciclo_guardado = CONFIG.get("ultimo_ciclo", "")

    # --- DECISIÓN: ¿PEDIMOS PLATA? ---
    # Pedimos si el ingreso es 0 (app nueva/reseteada) O si cambió el ciclo (llegó tu día de pago)
    if ingreso_actual <= 0 or ciclo_actual != ciclo_guardado:
        dialog = ctk.CTkInputDialog(text=f"¡Ciclo de gastos [{ciclo_actual}]!\nIngresa tu presupuesto para este periodo:", title="Presupuesto Inicial")
        respuesta = dialog.get_input()
        
        if respuesta and respuesta.replace(".", "").isdigit():
            ingreso_actual = int(respuesta.replace(".", ""))
            # 1. Anotamos que YA TE COBRAMOS este ciclo
            CONFIG["ultimo_ciclo"] = ciclo_actual
            # 2. Guardamos la memoria (config.json)
            guardar_config()
            # 3. Guardamos la plata real en tu base de datos de gastos (datos.json/txt)
            guardar_datos(ingreso_actual, gastos_actuales) 
            actualizar_pantalla()
        elif ingreso_actual <= 0:
            # Seguro por si el usuario cancela la ventana para que no quede en bucle
            ingreso_actual = 1
            guardar_datos(ingreso_actual, gastos_actuales)
            actualizar_pantalla()

def resetear_datos_gui():
    resp = messagebox.askyesno(t("aj_peligro"), "¿Estás 100% seguro de borrar TODO tu historial y tu presupuesto?")
    if resp:
        global ingreso_actual
        gastos_actuales.clear()  # Borra los gastos
        ingreso_actual = 0       # ¡ACÁ ESTÁ LA CLAVE! Vuelve la plata a cero
        guardar_datos(ingreso_actual, gastos_actuales)
        
        # Le borramos la memoria del día de pago
        CONFIG["ultimo_ciclo"] = ""
        guardar_config()
        
        mostrar_alerta("info", "Reinicio", "Historial borrado.\nEl programa se cerrará para que ingreses tu nuevo presupuesto.")
        app.destroy() # Cierra la app para forzar el inicio limpio

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

    # 1. Buscamos cuál es la clave interna de la categoría que seleccionó
    clave_real = next((k for k, v in TEXTOS[CONFIG["idioma"]].items() if v == categoria), categoria)
    limite = CONFIG.get("presupuestos_cat", {}).get(clave_real, 0)
    
    if limite > 0: # Solo funciona si el usuario configuró un límite mayor a 0
        mes_actual_str = datetime.now().strftime("%Y-%m")
        # Calculamos cuánto ha gastado en esta categoría ESTE MES
        gastos_mes_cat = sum(g["monto"] for g in gastos_actuales if g["fecha"].startswith(mes_actual_str) and g["categoria"] == categoria)
        
        if gastos_mes_cat + monto > limite:
            # ¡Se pasó del límite! Mostramos la advertencia
            mon = CONFIG["moneda"]
            mensaje = f"{t('txt_superado')} {categoria}!\n\nLímite: {mon}{limite:,}\nYa llevas: {mon}{gastos_mes_cat:,}\n+ Este gasto: {mon}{monto:,}\n\n{t('txt_guardar_igual')}"
            
            resp = messagebox.askyesno(t("msg_limite"), mensaje.replace(",", "."))
            if not resp:
                return # Si el usuario dice que NO, cortamos la función y no guarda nada

    gastos_actuales.append({
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "monto": monto,
        "categoria": categoria, 
        "descripcion": descripcion
    })
    
    guardar_datos(ingreso_actual, gastos_actuales)
    actualizar_pantalla()

    entrada_monto.delete(0, "end")
    entrada_desc.delete(0, "end")

def mostrar_acerca_de_gui():
    texto_about = f"{t('titulo')} V4.0\n\nDev: Mathias\nIngeniería Civil Informática\nUniversidad de Valparaíso"
    mostrar_alerta("info", t("btn_acerca"), texto_about)

def abrir_ventana_limites():
    ventana_limites = ctk.CTkToplevel(app)
    ventana_limites.title(t("btn_limites"))
    ventana_limites.geometry("400x500")
    ventana_limites.attributes("-topmost", True)

    lbl_tit = ctk.CTkLabel(ventana_limites, text=t("tit_limites"), font=("Arial", 16, "bold"))
    lbl_tit.pack(pady=15)

    frame_entradas = ctk.CTkFrame(ventana_limites, fg_color="transparent")
    frame_entradas.pack(fill="both", expand=True, padx=20)

    lista_categorias_claves = ["cat_comida", "cat_juegos", "cat_transporte", "cat_servicios", "cat_hogar", "cat_otros"]
    entradas = {}

    # Generar una caja de texto por cada categoría
    for idx, clave in enumerate(lista_categorias_claves):
        ctk.CTkLabel(frame_entradas, text=t(clave), font=("Arial", 14)).grid(row=idx, column=0, sticky="w", pady=10)
        
        ent = ctk.CTkEntry(frame_entradas, width=150, justify="right")
        # Mostrar el valor guardado o 0 si no hay
        valor_actual = CONFIG["presupuestos_cat"].get(clave, 0)
        ent.insert(0, str(valor_actual))
        ent.grid(row=idx, column=1, sticky="e", pady=10, padx=10)
        entradas[clave] = ent

    def guardar_limites():
        limites_temp = {}
        suma_total = 0
        
        # Primero recolectamos y sumamos todo antes de guardar
        for clave, ent in entradas.items():
            valor_str = ent.get().replace(".", "").strip()
            try:
                valor = int(valor_str) if valor_str.isdigit() else 0
            except:
                valor = 0
            limites_temp[clave] = valor
            suma_total += valor
            
        # --- EL SEGURO ANTICHOQUE FINANCIERO ---
        # Verificamos si la suma de los límites supera la plata real que tienes
        if suma_total > ingreso_actual:
            mon = CONFIG.get("moneda", "$")
            suma_fmt = f"{suma_total:,}".replace(",", ".")
            ingreso_fmt = f"{ingreso_actual:,}".replace(",", ".")
            
            mostrar_alerta("warning", "Presupuesto Excedido", 
                           f"¡Ojo compadre!\n\nLa suma de tus límites ({mon}{suma_fmt}) es mayor a tu presupuesto mensual ({mon}{ingreso_fmt}).\n\nBájale a los límites para no quedar en rojo a fin de mes.")
            return # El 'return' hace que se cancele el guardado y no cierre la ventana
            
        # Si las matemáticas cuadran, guardamos de verdad
        CONFIG["presupuestos_cat"] = limites_temp
        guardar_config()
        ventana_limites.destroy()
        mostrar_alerta("info", t("alerta_listo"), "Límites actualizados correctamente.")

    # --- BOTÓN PARA RESETEAR LA VISTA A CERO ---
    def limpiar_a_cero():
        for ent in entradas.values():
            ent.delete(0, "end")
            ent.insert(0, "0")

    btn_limpiar = ctk.CTkButton(ventana_limites, text="Limpiar todo a 0", command=limpiar_a_cero, fg_color="#7F8C8D", hover_color="#616A6B", font=("Arial", 14))
    btn_limpiar.pack(pady=(10, 5), fill="x", padx=20)

    btn_guardar_lim = ctk.CTkButton(ventana_limites, text="Guardar Límites", command=guardar_limites, fg_color="#E67E22", hover_color="#D35400", font=("Arial", 14, "bold"))
    btn_guardar_lim.pack(pady=(5, 20), fill="x", padx=20)

def configurar_dia_pago():
    dia_actual = CONFIG.get("dia_pago", 1)
    dialog = ctk.CTkInputDialog(text=f"¿Qué día del mes recibes tu sueldo/mesada?\nActualmente es el día: {dia_actual}\n\nIngresa un número (1 al 31):", title="Configurar Día de Pago")
    respuesta = dialog.get_input()
    
    if respuesta and respuesta.isdigit():
        dia = int(respuesta)
        if 1 <= dia <= 31:
            CONFIG["dia_pago"] = dia
            guardar_config()
            mostrar_alerta("info", "Día Actualizado", f"Perfecto. Ahora el presupuesto se renovará los días {dia} de cada mes.")
            verificar_primera_vez() # Revisa al tiro si corresponde pedir plata
        else:
            mostrar_alerta("warning", "Error", "Debe ser un número válido entre el 1 y el 31.") 

def abrir_ventana_buscar():
    ventana_buscar = ctk.CTkToplevel(app)
    ventana_buscar.title("🔍 " + t("tit_buscar"))
    ventana_buscar.geometry("750x600")
    ventana_buscar.attributes("-topmost", True)

    frame_filtros = ctk.CTkFrame(ventana_buscar)
    frame_filtros.pack(fill="x", padx=10, pady=10)

    # --- CAMBIO CLAVE: Ahora es un ScrollableFrame en vez de Textbox ---
    scroll_resultados = ctk.CTkScrollableFrame(ventana_buscar, fg_color="#1E1E1E")
    scroll_resultados.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # --- FUNCIÓN INTERNA PARA BORRAR ---
    def borrar_desde_buscador(gasto_a_borrar):
        # Confirmación
        resp = messagebox.askyesno(t("aj_peligro"), f"{t('msg_borrar')}\n\n{gasto_a_borrar['descripcion']} - {CONFIG['moneda']}{gasto_a_borrar['monto']}")
        if resp:
            gastos_actuales.remove(gasto_a_borrar)
            guardar_datos(ingreso_actual, gastos_actuales)
            actualizar_pantalla() # Actualiza el dashboard de fondo
            aplicar_busqueda()    # Refresca la lista de búsqueda al instante
            mostrar_alerta("info", t("alerta_listo"), t("alerta_borrado"))
            ventana_buscar.attributes("-topmost", True) # Asegurar que la ventana vuelva al frente tras la alerta

    # --- EL MOTOR DE BÚSQUEDA ---
    def aplicar_busqueda(event=None): 
        texto_buscar = ent_texto.get().strip().lower()
        monto_str = ent_monto.get().strip().replace(".", "")
        monto_min = int(monto_str) if monto_str.isdigit() else 0
        cat_sel = combo_cat.get()
        mes_sel = combo_mes.get()
        orden_sel = combo_orden.get()

        resultados = []
        for g in gastos_actuales:
            if g["monto"] < monto_min: continue
            if mes_sel != t("opt_todas") and not g["fecha"].startswith(mes_sel): continue
            if texto_buscar and texto_buscar not in g["descripcion"].lower() and texto_buscar not in g["categoria"].lower(): continue
            
            clave_real = next((k for k, v in TEXTOS["es"].items() if v == g["categoria"]), g["categoria"])
            if cat_sel != t("opt_todas") and t(clave_real) != cat_sel: continue
            resultados.append(g)

        # Ordenar
        if orden_sel == t("ord_fecha_desc"): resultados.sort(key=lambda x: x["fecha"], reverse=True)
        elif orden_sel == t("ord_fecha_asc"): resultados.sort(key=lambda x: x["fecha"])
        elif orden_sel == t("ord_monto_desc"): resultados.sort(key=lambda x: x["monto"], reverse=True)
        elif orden_sel == t("ord_monto_asc"): resultados.sort(key=lambda x: x["monto"])

        # LIMPIAR RESULTADOS ANTERIORES
        for widget in scroll_resultados.winfo_children():
            widget.destroy()
        
        if not resultados:
            ctk.CTkLabel(scroll_resultados, text="No se encontraron gastos con esta búsqueda...", font=("Arial", 14, "italic")).pack(pady=20)
        else:
            total_filtrado = 0
            mon = CONFIG["moneda"]
            for g in resultados:
                total_filtrado += g["monto"]
                monto_fmt = f"{g['monto']:,}".replace(",", ".")
                clave_real = next((k for k, v in TEXTOS["es"].items() if v == g["categoria"]), g["categoria"])
                cat_trad = t(clave_real)
                
                # Crear Fila
                fila = ctk.CTkFrame(scroll_resultados, fg_color="transparent")
                fila.pack(fill="x", pady=2, padx=5)
                
                texto_item = f"[{g['fecha']}] {cat_trad}: {mon}{monto_fmt} - {g['descripcion']}"
                lbl_texto = ctk.CTkLabel(fila, text=texto_item, font=("Arial", 14), anchor="w")
                lbl_texto.pack(side="left", fill="x", expand=True)
                
                # El truco: lambda gasto=g asegura que el botón sepa exactamente a qué gasto apuntar
                btn_del = ctk.CTkButton(fila, text="🗑️", width=35, fg_color="#C0392B", hover_color="#922B21", 
                                        command=lambda gasto=g: borrar_desde_buscador(gasto))
                btn_del.pack(side="right")
            
            # Línea de Total
            total_fmt = f"{total_filtrado:,}".replace(",", ".")
            ctk.CTkFrame(scroll_resultados, height=2, fg_color="gray").pack(fill="x", pady=(15, 5))
            lbl_total = ctk.CTkLabel(scroll_resultados, text=f"TOTAL ENCONTRADO: {mon}{total_fmt}", font=("Arial", 16, "bold"))
            lbl_total.pack(anchor="w", padx=5)

    # --- INTERFAZ DE FILTROS ---
    ctk.CTkLabel(frame_filtros, text=t("lbl_busqueda")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ent_texto = ctk.CTkEntry(frame_filtros, width=200, placeholder_text="Ej: Steam, comida...")
    ent_texto.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(frame_filtros, text=t("lbl_monto_min")).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    ent_monto = ctk.CTkEntry(frame_filtros, width=150, placeholder_text="Ej: 10000")
    ent_monto.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(frame_filtros, text=t("lbl_filtro_cat")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    cat_loc = [t("opt_todas"), t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")]
    combo_cat = ctk.CTkComboBox(frame_filtros, values=cat_loc, width=200)
    combo_cat.set(t("opt_todas"))
    combo_cat.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(frame_filtros, text=t("lbl_filtro_mes")).grid(row=1, column=2, padx=5, pady=5, sticky="e")
    meses_disp = [t("opt_todas")] + obtener_meses_disponibles()
    combo_mes = ctk.CTkComboBox(frame_filtros, values=meses_disp, width=150)
    combo_mes.set(t("opt_todas"))
    combo_mes.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(frame_filtros, text=t("lbl_orden")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    ord_loc = [t("ord_fecha_desc"), t("ord_fecha_asc"), t("ord_monto_desc"), t("ord_monto_asc")]
    combo_orden = ctk.CTkComboBox(frame_filtros, values=ord_loc, width=200)
    combo_orden.set(t("ord_fecha_desc"))
    combo_orden.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    btn_filtro = ctk.CTkButton(frame_filtros, text="🔍 BUSCAR", fg_color="#2980B9", hover_color="#1F618D", font=("Arial", 14, "bold"), height=35, command=aplicar_busqueda)
    btn_filtro.grid(row=2, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

    ventana_buscar.bind('<Return>', aplicar_busqueda)
    aplicar_busqueda()

def restaurar_fabrica_gui():
    resp = messagebox.askyesno(t("aj_peligro"), "¿Volver a la configuración predeterminada? / Restore default settings?")
    if resp:
        if ARCHIVO_CONFIG.exists(): 
            ARCHIVO_CONFIG.unlink()
        mostrar_alerta("info", "Reinicio / Restart", "El programa se cerrará para aplicar los cambios.")
        app.destroy() # Cerramos el programa entero para forzar el reinicio


# --- 5. ARRANQUE PRINCIPAL ---
cargar_config()

app = ctk.CTk()
app.geometry("1150x700")
app.minsize(1000, 650)

# --- NUEVO: CIERRE LIMPIO PARA EVITAR ERRORES FANTASMAS ---
def cerrar_programa():
    app.quit()    # 1. Detiene todos los procesos y animaciones de fondo
    app.destroy() # 2. Ahora sí, destruye la ventana de forma segura

# Le decimos a la "X" de la ventana que use esta función
app.protocol("WM_DELETE_WINDOW", cerrar_programa)

# --- NUEVO: SISTEMA DE GRILLA (GRID) ANTI-APLASTAMIENTO ---
app.grid_columnconfigure(0, weight=0) # Columna izquierda rígida (no crece ni se achica)
app.grid_columnconfigure(1, weight=1) # Columna derecha expansible (toma el resto del espacio)
app.grid_rowconfigure(0, weight=1)    # Que ocupe todo el alto de la pantalla

# --- LA NUEVA MAGIA DEL MENÚ DINÁMICO ---
barra_menu = tk.Menu(app)
app.config(menu=barra_menu)

var_zoom = tk.StringVar(value=CONFIG.get("zoom", "100%"))
var_tema = tk.StringVar(value=CONFIG.get("tema", "Oscuro"))
var_moneda = tk.StringVar(value=CONFIG.get("moneda", "$"))
var_alertas = tk.BooleanVar(value=CONFIG.get("alertas", True))
var_idioma = tk.StringVar(value=CONFIG.get("idioma", "es"))

def set_zoom_menu(valor):
    CONFIG["zoom"] = valor
    escala = float(valor.replace("%", "")) / 100
    ctk.set_widget_scaling(escala)
    ctk.set_window_scaling(escala)
    guardar_config()

def set_tema_menu(valor):
    CONFIG["tema"] = valor
    ctk.set_appearance_mode("dark" if valor == "Oscuro" else "light")
    guardar_config()
    actualizar_pantalla()

def set_moneda_menu(valor):
    CONFIG["moneda"] = valor
    guardar_config()
    actualizar_pantalla()

def toggle_alertas_menu():
    CONFIG["alertas"] = var_alertas.get()
    guardar_config()

def cambiar_ruta_menu():
    nueva_ruta = filedialog.askdirectory(title=t("btn_cambiar_ruta"))
    if nueva_ruta:
        ruta_antigua = obtener_ruta_archivo()
        CONFIG["ruta_datos"] = nueva_ruta
        ruta_nueva = obtener_ruta_archivo()
        if ruta_antigua.exists() and str(ruta_antigua) != str(ruta_nueva):
            shutil.move(str(ruta_antigua), str(ruta_nueva))
        guardar_config()
        mostrar_alerta("info", t("alerta_listo"), "Ruta actualizada.")

def set_idioma_menu(codigo):
    CONFIG["idioma"] = codigo
    var_idioma.set(codigo)
    guardar_config()
    aplicar_textos_ui()
    construir_menu() # Magia: Si cambias idioma, el menú se borra y se re-traduce solo al instante

def construir_menu():
    barra_menu.delete(0, "end") 
    
    # 1. Archivo
    menu_archivo = tk.Menu(barra_menu, tearoff=0)
    menu_archivo.add_command(label=t("menu_salir"), command=cerrar_programa)
    barra_menu.add_cascade(label=t("menu_arch"), menu=menu_archivo)

    # 2. Herramientas
    menu_herramientas = tk.Menu(barra_menu, tearoff=0)
    
    menu_zoom = tk.Menu(menu_herramientas, tearoff=0)
    for z in ["80%", "100%", "125%", "150%"]:
        menu_zoom.add_radiobutton(label=z, variable=var_zoom, value=z, command=lambda v=z: set_zoom_menu(v))
    menu_herramientas.add_cascade(label=t("aj_zoom"), menu=menu_zoom)
    
    menu_tema = tk.Menu(menu_herramientas, tearoff=0)
    menu_tema.add_radiobutton(label="Claro / Light", variable=var_tema, value="Claro", command=lambda: set_tema_menu("Claro"))
    menu_tema.add_radiobutton(label="Oscuro / Dark", variable=var_tema, value="Oscuro", command=lambda: set_tema_menu("Oscuro"))
    menu_herramientas.add_cascade(label=t("aj_tema"), menu=menu_tema)

    menu_moneda = tk.Menu(menu_herramientas, tearoff=0)
    for m in ["$", "US$", "€", "£"]:
        menu_moneda.add_radiobutton(label=m, variable=var_moneda, value=m, command=lambda v=m: set_moneda_menu(v))
    menu_herramientas.add_cascade(label=t("aj_moneda"), menu=menu_moneda)

    menu_herramientas.add_checkbutton(label=t("aj_alertas"), variable=var_alertas, command=toggle_alertas_menu)
    menu_herramientas.add_separator()
    menu_herramientas.add_command(label=t("aj_ruta"), command=cambiar_ruta_menu)
    menu_herramientas.add_command(label="Día de Pago (Mensual)", command=configurar_dia_pago)
    menu_herramientas.add_command(label=t("btn_limites"), command=abrir_ventana_limites)
    menu_herramientas.add_command(label=t("btn_restaurar"), command=restaurar_fabrica_gui)
    menu_herramientas.add_command(label=t("btn_reset"), command=resetear_datos_gui)
    barra_menu.add_cascade(label=t("menu_herr"), menu=menu_herramientas)

    # 3. Ayuda
    menu_ayu = tk.Menu(barra_menu, tearoff=0)
    menu_ayu.add_command(label=t("btn_acerca"), command=mostrar_acerca_de_gui)
    barra_menu.add_cascade(label=t("menu_ayu"), menu=menu_ayu)

    # 4. Idioma
    menu_idioma = tk.Menu(barra_menu, tearoff=0)
    idiomas_disp = {"Español": "es", "English": "en", "Português": "pt", "Français": "fr", "Italiano": "it", "Deutsch": "de"}
    for nom, cod in idiomas_disp.items():
        menu_idioma.add_radiobutton(label=nom, variable=var_idioma, value=cod, command=lambda c=cod: set_idioma_menu(c))
    barra_menu.add_cascade(label=t("menu_idi"), menu=menu_idioma)

construir_menu() # Arranca el menú por primera vez

# --- PANELES CON EL NUEVO SISTEMA GRID ---
frame_izquierdo = ctk.CTkFrame(app, width=320) # Ancho fijo
frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
frame_izquierdo.grid_propagate(False) # MAGIA: Congela el panel izquierdo para que NADA lo aplaste

frame_derecho = ctk.CTkFrame(app)
frame_derecho.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)

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

btn_buscar = ctk.CTkButton(frame_izquierdo, text="", command=abrir_ventana_buscar, fg_color="#8E44AD", hover_color="#732D91", font=("Arial", 12, "bold"))
btn_buscar.pack(pady=5, padx=20, fill="x")

# PANEL DERECHO
seg_periodos = ctk.CTkSegmentedButton(frame_derecho, command=actualizar_pantalla)
seg_periodos.pack(pady=(20, 5), padx=20, fill="x")

lbl_dash_mes = ctk.CTkLabel(frame_derecho, text="📊 Resumen", font=("Arial", 28, "bold"))
lbl_dash_mes.pack(pady=(0, 10))

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

texto_historial = ctk.CTkTextbox(frame_derecho, state="disabled", font=("Arial", 14), height=180)
texto_historial.pack(fill="both", expand=True, padx=20, pady=(0, 20))

construir_menu()
aplicar_textos_ui()
app.after(100, verificar_primera_vez)
app.mainloop()