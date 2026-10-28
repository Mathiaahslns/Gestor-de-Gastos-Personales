import sys
import json
import csv
import shutil
import os
import subprocess
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
    CONFIG["presupuestos_cat"] = {} 

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

# --- INYECTOR 5: TEXTOS HUÉRFANOS (Límites, Días y Reset) ---
nuevos_textos_huerfanos = {
    "es": {
        "tit_presupuesto": "Presupuesto Inicial", "msg_ciclo_1": "¡Ciclo de gastos [", "msg_ciclo_2": "]!\nIngresa tu presupuesto para este periodo:",
        "lbl_total_enc": "TOTAL ENCONTRADO:", "menu_dia_pago": "Día de Pago (Mensual)",
        "tit_dia_pago": "Configurar Día de Pago", "msg_dia_pago_1": "¿Qué día del mes recibes tu sueldo/mesada?\nActualmente es el día: ", "msg_dia_pago_2": "\n\nIngresa un número (1 al 31):",
        "tit_dia_act": "Día Actualizado", "msg_dia_ok_1": "Perfecto. Ahora el presupuesto se renovará los días ", "msg_dia_ok_2": " de cada mes.", "err_dia": "Debe ser un número válido entre el 1 y el 31.",
        "btn_limpiar_0": "Limpiar todo a 0", "btn_guardar_lim_2": "Guardar Límites", "msg_limites_ok": "Límites actualizados correctamente.",
        "tit_pres_exc": "Presupuesto Excedido", "msg_pres_exc_1": "¡Ojo compadre!\n\nLa suma de tus límites (", "msg_pres_exc_2": ") es mayor a tu presupuesto mensual (", "msg_pres_exc_3": ").\n\nBájale a los límites para no quedar en rojo a fin de mes.",
        "msg_reset_seguro": "¿Estás 100% seguro de borrar TODO tu historial y tu presupuesto?", "tit_reinicio": "Reinicio", "msg_reinicio": "Historial borrado.\nEl programa se cerrará para que ingreses tu nuevo presupuesto."
    },
    "en": {
        "tit_presupuesto": "Initial Budget", "msg_ciclo_1": "Expense cycle [", "msg_ciclo_2": "]!\nEnter your budget for this period:",
        "lbl_total_enc": "TOTAL FOUND:", "menu_dia_pago": "Payday (Monthly)",
        "tit_dia_pago": "Set Payday", "msg_dia_pago_1": "What day of the month do you get paid?\nCurrently it is day: ", "msg_dia_pago_2": "\n\nEnter a number (1 to 31):",
        "tit_dia_act": "Day Updated", "msg_dia_ok_1": "Perfect. The budget will now renew on day ", "msg_dia_ok_2": " of every month.", "err_dia": "Must be a valid number between 1 and 31.",
        "btn_limpiar_0": "Clear all to 0", "btn_guardar_lim_2": "Save Limits", "msg_limites_ok": "Limits updated correctly.",
        "tit_pres_exc": "Budget Exceeded", "msg_pres_exc_1": "Watch out!\n\nThe sum of your limits (", "msg_pres_exc_2": ") is greater than your monthly budget (", "msg_pres_exc_3": ").\n\nLower the limits to avoid going into the red.",
        "msg_reset_seguro": "Are you 100% sure you want to delete ALL your history and budget?", "tit_reinicio": "Restart", "msg_reinicio": "History deleted.\nThe program will close so you can enter your new budget."
    },
    "pt": {
        "tit_presupuesto": "Orçamento Inicial", "msg_ciclo_1": "Ciclo de despesas [", "msg_ciclo_2": "]!\nInsira seu orçamento para este período:",
        "lbl_total_enc": "TOTAL ENCONTRADO:", "menu_dia_pago": "Dia de Pagamento (Mensal)",
        "tit_dia_pago": "Configurar Dia de Pagamento", "msg_dia_pago_1": "Que dia do mês você recebe seu salário?\nAtualmente é o dia: ", "msg_dia_pago_2": "\n\nInsira um número (1 a 31):",
        "tit_dia_act": "Dia Atualizado", "msg_dia_ok_1": "Perfeito. O orçamento será renovado nos dias ", "msg_dia_ok_2": " de cada mês.", "err_dia": "Deve ser um número válido entre 1 e 31.",
        "btn_limpiar_0": "Limpar tudo para 0", "btn_guardar_lim_2": "Salvar Limites", "msg_limites_ok": "Limites atualizados corretamente.",
        "tit_pres_exc": "Orçamento Excedido", "msg_pres_exc_1": "Atenção!\n\nA soma dos seus limites (", "msg_pres_exc_2": ") é maior que o seu orçamento mensal (", "msg_pres_exc_3": ").\n\nReduza os limites para não ficar no vermelho.",
        "msg_reset_seguro": "Tem certeza de que deseja apagar TODO o seu histórico e orçamento?", "tit_reinicio": "Reiniciar", "msg_reinicio": "Histórico apagado.\nO programa será fechado para que você insira seu novo orçamento."
    },
    "fr": {
        "tit_presupuesto": "Budget Initial", "msg_ciclo_1": "Cycle de dépenses [", "msg_ciclo_2": "]!\nEntrez votre budget pour cette période:",
        "lbl_total_enc": "TOTAL TROUVÉ:", "menu_dia_pago": "Jour de Paie (Mensuel)",
        "tit_dia_pago": "Configurer le Jour de Paie", "msg_dia_pago_1": "Quel jour du mois êtes-vous payé?\nActuellement c'est le jour: ", "msg_dia_pago_2": "\n\nEntrez un nombre (1 à 31):",
        "tit_dia_act": "Jour Mis à Jour", "msg_dia_ok_1": "Parfait. Le budget sera renouvelé le ", "msg_dia_ok_2": " de chaque mois.", "err_dia": "Doit être un nombre valide entre 1 et 31.",
        "btn_limpiar_0": "Tout remettre à 0", "btn_guardar_lim_2": "Enregistrer les Limites", "msg_limites_ok": "Limites mises à jour correctement.",
        "tit_pres_exc": "Budget Dépassé", "msg_pres_exc_1": "Attention!\n\nLa somme de vos limites (", "msg_pres_exc_2": ") est supérieure à votre budget mensuel (", "msg_pres_exc_3": ").\n\nBaissez les limites pour éviter d'être à découvert.",
        "msg_reset_seguro": "Êtes-vous sûr à 100% de vouloir supprimer TOUT votre historique et budget?", "tit_reinicio": "Redémarrer", "msg_reinicio": "Historique supprimé.\nLe programme va se fermer pour que vous puissiez entrer votre nouveau budget."
    },
    "it": {
        "tit_presupuesto": "Budget Iniziale", "msg_ciclo_1": "Ciclo di spesa [", "msg_ciclo_2": "]!\nInserisci il tuo budget per questo periodo:",
        "lbl_total_enc": "TOTALE TROVATO:", "menu_dia_pago": "Giorno di Paga (Mensile)",
        "tit_dia_pago": "Imposta Giorno di Paga", "msg_dia_pago_1": "In quale giorno del mese vieni pagato?\nAttualmente è il giorno: ", "msg_dia_pago_2": "\n\nInserisci un numero (da 1 a 31):",
        "tit_dia_act": "Giorno Aggiornato", "msg_dia_ok_1": "Perfetto. Il budget si rinnoverà il giorno ", "msg_dia_ok_2": " di ogni mese.", "err_dia": "Deve essere un numero valido tra 1 e 31.",
        "btn_limpiar_0": "Azzera tutto", "btn_guardar_lim_2": "Salva Limiti", "msg_limites_ok": "Limiti aggiornati correttamente.",
        "tit_pres_exc": "Budget Superato", "msg_pres_exc_1": "Attenzione!\n\nLa somma dei tuoi limiti (", "msg_pres_exc_2": ") è maggiore del tuo budget mensile (", "msg_pres_exc_3": ").\n\nAbbassa i limiti per non andare in rosso.",
        "msg_reset_seguro": "Sei sicuro al 100% di voler eliminare TUTTA la tua cronologia e il budget?", "tit_reinicio": "Riavvia", "msg_reinicio": "Cronologia eliminata.\nIl programma si chiuderà per permetterti di inserire il nuovo budget."
    },
    "de": {
        "tit_presupuesto": "Anfangsbudget", "msg_ciclo_1": "Ausgabenzyklus [", "msg_ciclo_2": "]!\nGeben Sie Ihr Budget für diesen Zeitraum ein:",
        "lbl_total_enc": "GESAMT GEFUNDEN:", "menu_dia_pago": "Zahltag (Monatlich)",
        "tit_dia_pago": "Zahltag Festlegen", "msg_dia_pago_1": "An welchem Tag im Monat werden Sie bezahlt?\nAktuell ist es Tag: ", "msg_dia_pago_2": "\n\nGeben Sie eine Zahl ein (1 bis 31):",
        "tit_dia_act": "Tag Aktualisiert", "msg_dia_ok_1": "Perfekt. Das Budget wird nun am ", "msg_dia_ok_2": ". jeden Monats erneuert.", "err_dia": "Muss eine gültige Zahl zwischen 1 und 31 sein.",
        "btn_limpiar_0": "Alles auf 0 setzen", "btn_guardar_lim_2": "Limits Speichern", "msg_limites_ok": "Limits erfolgreich aktualisiert.",
        "tit_pres_exc": "Budget Überschritten", "msg_pres_exc_1": "Achtung!\n\nDie Summe Ihrer Limits (", "msg_pres_exc_2": ") ist größer als Ihr monatliches Budget (", "msg_pres_exc_3": ").\n\nSenken Sie die Limits, um rote Zahlen zu vermeiden.",
        "msg_reset_seguro": "Sind Sie zu 100% sicher, dass Sie Ihren GESAMTEN Verlauf und Ihr Budget löschen möchten?", "tit_reinicio": "Neustart", "msg_reinicio": "Verlauf gelöscht.\nDas Programm wird geschlossen, damit Sie Ihr neues Budget eingeben können."
    }
}
for lang, dic in nuevos_textos_huerfanos.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 6: EXPORTACIÓN DE DATOS ---
nuevos_textos_exportar = {
    "es": {"menu_exportar": "Exportar Datos", "exp_csv": "Exportar como CSV", "exp_excel": "Exportar como Excel (.xlsx)", "exp_txt": "Exportar como TXT", "msg_exp_ok": "Datos exportados correctamente en:\n", "msg_exp_err": "Error al exportar:\n", "err_excel": "Necesitas instalar 'openpyxl' para exportar a Excel.\nAbre la terminal y ejecuta:\npip install openpyxl"},
    "en": {"menu_exportar": "Export Data", "exp_csv": "Export as CSV", "exp_excel": "Export as Excel (.xlsx)", "exp_txt": "Export as TXT", "msg_exp_ok": "Data exported successfully to:\n", "msg_exp_err": "Error exporting:\n", "err_excel": "You need to install 'openpyxl' to export to Excel.\nOpen terminal and run:\npip install openpyxl"},
    "pt": {"menu_exportar": "Exportar Dados", "exp_csv": "Exportar como CSV", "exp_excel": "Exportar como Excel (.xlsx)", "exp_txt": "Exportar como TXT", "msg_exp_ok": "Dados exportados com sucesso em:\n", "msg_exp_err": "Erro ao exportar:\n", "err_excel": "Você precisa instalar 'openpyxl' para exportar para Excel.\nAbra o terminal e execute:\npip install openpyxl"},
    "fr": {"menu_exportar": "Exporter les Données", "exp_csv": "Exporter en CSV", "exp_excel": "Exporter en Excel (.xlsx)", "exp_txt": "Exporter en TXT", "msg_exp_ok": "Données exportées avec succès dans:\n", "msg_exp_err": "Erreur lors de l'exportation:\n", "err_excel": "Vous devez installer 'openpyxl' pour exporter vers Excel.\nOuvrez le terminal et exécutez:\npip install openpyxl"},
    "it": {"menu_exportar": "Esporta Dati", "exp_csv": "Esporta come CSV", "exp_excel": "Esporta come Excel (.xlsx)", "exp_txt": "Esporta come TXT", "msg_exp_ok": "Dati esportati con successo in:\n", "msg_exp_err": "Errore durante l'esportazione:\n", "err_excel": "Devi installare 'openpyxl' per esportare in Excel.\nApri il terminale ed esegui:\npip install openpyxl"},
    "de": {"menu_exportar": "Daten Exportieren", "exp_csv": "Als CSV exportieren", "exp_excel": "Als Excel exportieren (.xlsx)", "exp_txt": "Als TXT exportieren", "msg_exp_ok": "Daten erfolgreich exportiert nach:\n", "msg_exp_err": "Fehler beim Exportieren:\n", "err_excel": "Sie müssen 'openpyxl' installieren, um nach Excel zu exportieren.\nIm Terminal ausführen:\npip install openpyxl"}
}
for lang, dic in nuevos_textos_exportar.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 7: ENCABEZADOS DE EXPORTACIÓN ---
nuevos_textos_columnas = {
    "es": {"col_fecha": "Fecha", "col_cat": "Categoría", "col_monto": "Monto", "col_desc": "Descripción"},
    "en": {"col_fecha": "Date", "col_cat": "Category", "col_monto": "Amount", "col_desc": "Description"},
    "pt": {"col_fecha": "Data", "col_cat": "Categoria", "col_monto": "Valor", "col_desc": "Descrição"},
    "fr": {"col_fecha": "Date", "col_cat": "Catégorie", "col_monto": "Montant", "col_desc": "Description"},
    "it": {"col_fecha": "Data", "col_cat": "Categoria", "col_monto": "Importo", "col_desc": "Descrizione"},
    "de": {"col_fecha": "Datum", "col_cat": "Kategorie", "col_monto": "Betrag", "col_desc": "Beschreibung"}
}
for lang, dic in nuevos_textos_columnas.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 8: BACKUP Y RESTAURACIÓN ---
nuevos_textos_backup = {
    "es": {"menu_backup": "Crear Copia de Seguridad", "menu_restaurar": "Restaurar Copia", "tit_backup": "Guardar Backup", "tit_restaurar": "Abrir Backup", "msg_backup_ok": "Copia de seguridad guardada con éxito en:\n", "msg_restaurar_ok": "Copia de seguridad restaurada con éxito.\nEl dashboard ha sido actualizado.", "err_backup_leer": "El archivo seleccionado no es un backup válido o está corrupto.", "msg_conf_restaurar": "¿Sobrescribir tus datos actuales con esta copia de seguridad?", "err_general": "Se produjo un error:\n"},
    "en": {"menu_backup": "Create Backup", "menu_restaurar": "Restore Backup", "tit_backup": "Save Backup", "tit_restaurar": "Open Backup", "msg_backup_ok": "Backup successfully saved to:\n", "msg_restaurar_ok": "Backup successfully restored.\nDashboard has been updated.", "err_backup_leer": "The selected file is not a valid backup or is corrupted.", "msg_conf_restaurar": "Overwrite your current data with this backup?", "err_general": "An error occurred:\n"},
    "pt": {"menu_backup": "Criar Backup", "menu_restaurar": "Restaurar Backup", "tit_backup": "Salvar Backup", "tit_restaurar": "Abrir Backup", "msg_backup_ok": "Backup salvo com sucesso em:\n", "msg_restaurar_ok": "Backup restaurado com sucesso.\nO painel foi atualizado.", "err_backup_leer": "O arquivo selecionado não é um backup válido ou está corrompido.", "msg_conf_restaurar": "Sobrescrever seus dados atuais com este backup?", "err_general": "Ocorreu um erro:\n"},
    "fr": {"menu_backup": "Créer une Sauvegarde", "menu_restaurar": "Restaurer la Sauvegarde", "tit_backup": "Enregistrer Sauvegarde", "tit_restaurar": "Ouvrir Sauvegarde", "msg_backup_ok": "Sauvegarde enregistrée avec succès dans:\n", "msg_restaurar_ok": "Sauvegarde restaurée avec succès.\nLe tableau de bord a été mis à jour.", "err_backup_leer": "Le fichier sélectionné n'est pas une sauvegarde valide ou est corrompu.", "msg_conf_restaurar": "Écraser vos données actuelles avec cette sauvegarde?", "err_general": "Une erreur est survenue:\n"},
    "it": {"menu_backup": "Crea Backup", "menu_restaurar": "Ripristina Backup", "tit_backup": "Salva Backup", "tit_restaurar": "Apri Backup", "msg_backup_ok": "Backup salvato con successo in:\n", "msg_restaurar_ok": "Backup ripristinato con successo.\nLa dashboard è stata aggiornata.", "err_backup_leer": "Il file selezionato non è un backup valido o è danneggiato.", "msg_conf_restaurar": "Sovrascrivere i tuoi dati attuali con questo backup?", "err_general": "Si è verificato un errore:\n"},
    "de": {"menu_backup": "Backup Erstellen", "menu_restaurar": "Backup Wiederherstellen", "tit_backup": "Backup Speichern", "tit_restaurar": "Backup Öffnen", "msg_backup_ok": "Backup erfolgreich gespeichert unter:\n", "msg_restaurar_ok": "Backup erfolgreich wiederhergestellt.\nDashboard wurde aktualisiert.", "err_backup_leer": "Die ausgewählte Datei ist kein gültiges Backup oder ist beschädigt.", "msg_conf_restaurar": "Ihre aktuellen Daten mit diesem Backup überschreiben?", "err_general": "Ein Fehler ist aufgetreten:\n"}
}
for lang, dic in nuevos_textos_backup.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 9: RESTAURAR AJUSTES DE FÁBRICA ---
nuevos_textos_fabrica = {
    "es": {"msg_conf_fabrica": "¿Volver a la configuración predeterminada?", "tit_reinicio_fab": "Reinicio", "msg_reinicio_fab": "El programa se cerrará para aplicar los cambios."},
    "en": {"msg_conf_fabrica": "Restore default settings?", "tit_reinicio_fab": "Restart", "msg_reinicio_fab": "The program will close to apply the changes."},
    "pt": {"msg_conf_fabrica": "Restaurar as configurações padrão?", "tit_reinicio_fab": "Reiniciar", "msg_reinicio_fab": "O programa será fechado para aplicar as alterações."},
    "fr": {"msg_conf_fabrica": "Restaurer les paramètres par défaut?", "tit_reinicio_fab": "Redémarrer", "msg_reinicio_fab": "Le programme va se fermer pour appliquer les modifications."},
    "it": {"msg_conf_fabrica": "Tornare alle impostazioni predefinite?", "tit_reinicio_fab": "Riavvia", "msg_reinicio_fab": "Il programma si chiuderà per applicare le modifiche."},
    "de": {"msg_conf_fabrica": "Standardeinstellungen wiederherstellen?", "tit_reinicio_fab": "Neustart", "msg_reinicio_fab": "Das Programm wird geschlossen, um die Änderungen anzuwenden."}
}
for lang, dic in nuevos_textos_fabrica.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 10: CATEGORÍAS PERSONALIZADAS ---
if "categorias_custom" not in CONFIG:
    CONFIG["categorias_custom"] = [] # Creamos el espacio en la memoria si no existe

nuevos_textos_cat_custom = {
    "es": {"menu_add_cat": "Agregar Categoría", "tit_add_cat": "Nueva Categoría", "msg_add_cat": "Ingresa el nombre de la nueva categoría (ej: Mascotas 🐶):", "msg_cat_ok": "Categoría agregada exitosamente.", "msg_cat_existe": "Esta categoría ya existe.", "err_cat_vacia": "El nombre no puede estar vacío."},
    "en": {"menu_add_cat": "Add Category", "tit_add_cat": "New Category", "msg_add_cat": "Enter the name of the new category (e.g., Pets 🐶):", "msg_cat_ok": "Category added successfully.", "msg_cat_existe": "This category already exists.", "err_cat_vacia": "Name cannot be empty."},
    "pt": {"menu_add_cat": "Adicionar Categoria", "tit_add_cat": "Nova Categoria", "msg_add_cat": "Digite o nome da nova categoria (ex: Pets 🐶):", "msg_cat_ok": "Categoria adicionada com sucesso.", "msg_cat_existe": "Esta categoria já existe.", "err_cat_vacia": "O nome não pode estar vazio."},
    "fr": {"menu_add_cat": "Ajouter Catégorie", "tit_add_cat": "Nouvelle Catégorie", "msg_add_cat": "Entrez le nom de la nouvelle catégorie (ex: Animaux 🐶):", "msg_cat_ok": "Catégorie ajoutée avec succès.", "msg_cat_existe": "Cette catégorie existe déjà.", "err_cat_vacia": "Le nom ne peut pas être vide."},
    "it": {"menu_add_cat": "Aggiungi Categoria", "tit_add_cat": "Nuova Categoria", "msg_add_cat": "Inserisci il nome della nuova categoria (es: Animali 🐶):", "msg_cat_ok": "Categoria aggiunta con successo.", "msg_cat_existe": "Questa categoria esiste già.", "err_cat_vacia": "Il nome non può essere vuoto."},
    "de": {"menu_add_cat": "Kategorie Hinzufügen", "tit_add_cat": "Neue Kategorie", "msg_add_cat": "Geben Sie den Namen der neuen Kategorie ein (z.B. Haustiere 🐶):", "msg_cat_ok": "Kategorie erfolgreich hinzugefügt.", "msg_cat_existe": "Diese Kategorie existiert bereits.", "err_cat_vacia": "Name darf nicht leer sein."}
}
for lang, dic in nuevos_textos_cat_custom.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 11: ELIMINAR CATEGORÍAS PERSONALIZADAS ---
nuevos_textos_del_cat = {
    "es": {"menu_del_cat": "Eliminar Categoría", "tit_del_cat": "Eliminar Categoría", "msg_no_custom_cat": "No hay categorías personalizadas para eliminar.", "lbl_sel_del_cat": "Selecciona la categoría a eliminar:", "msg_conf_del_cat": "¿Seguro que deseas eliminar la categoría '{}'?\n\n(Los gastos previos con este nombre no se borrarán)", "msg_cat_del_ok": "Categoría eliminada con éxito."},
    "en": {"menu_del_cat": "Delete Category", "tit_del_cat": "Delete Category", "msg_no_custom_cat": "No custom categories to delete.", "lbl_sel_del_cat": "Select category to delete:", "msg_conf_del_cat": "Are you sure you want to delete the category '{}'?\n\n(Previous expenses will not be deleted)", "msg_cat_del_ok": "Category deleted successfully."},
    "pt": {"menu_del_cat": "Excluir Categoria", "tit_del_cat": "Excluir Categoria", "msg_no_custom_cat": "Nenhuma categoria personalizada para excluir.", "lbl_sel_del_cat": "Selecione a categoria para excluir:", "msg_conf_del_cat": "Tem certeza de que deseja excluir a categoria '{}'?\n\n(Despesas anteriores não serão excluídas)", "msg_cat_del_ok": "Categoria excluída com sucesso."},
    "fr": {"menu_del_cat": "Supprimer Catégorie", "tit_del_cat": "Supprimer Catégorie", "msg_no_custom_cat": "Aucune catégorie personnalisée à supprimer.", "lbl_sel_del_cat": "Sélectionnez la catégorie à supprimer:", "msg_conf_del_cat": "Êtes-vous sûr de vouloir supprimer la catégorie '{}'?\n\n(Les dépenses précédentes ne seront pas supprimées)", "msg_cat_del_ok": "Catégorie supprimée avec succès."},
    "it": {"menu_del_cat": "Elimina Categoria", "tit_del_cat": "Elimina Categoria", "msg_no_custom_cat": "Nessuna categoria personalizzata da eliminare.", "lbl_sel_del_cat": "Seleziona la categoria da eliminare:", "msg_conf_del_cat": "Sei sicuro di voler eliminare la categoria '{}'?\n\n(Le spese precedenti non verranno eliminate)", "msg_cat_del_ok": "Categoria eliminata con successo."},
    "de": {"menu_del_cat": "Kategorie Löschen", "tit_del_cat": "Kategorie Löschen", "msg_no_custom_cat": "Keine benutzerdefinierten Kategorien zum Löschen.", "lbl_sel_del_cat": "Kategorie zum Löschen auswählen:", "msg_conf_del_cat": "Möchten Sie die Kategorie '{}' wirklich löschen?\n\n(Vorherige Ausgaben werden nicht gelöscht)", "msg_cat_del_ok": "Kategorie erfolgreich gelöscht."}
}
for lang, dic in nuevos_textos_del_cat.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 12: EDITAR GASTOS ---
nuevos_textos_editar = {
    "es": {"btn_editar": "✏️ Editar", "tit_editar": "Editar Gasto", "msg_edit_ok": "Gasto actualizado con éxito."},
    "en": {"btn_editar": "✏️ Edit", "tit_editar": "Edit Expense", "msg_edit_ok": "Expense updated successfully."},
    "pt": {"btn_editar": "✏️ Editar", "tit_editar": "Editar Despesa", "msg_edit_ok": "Despesa atualizada com sucesso."},
    "fr": {"btn_editar": "✏️ Éditer", "tit_editar": "Modifier Dépense", "msg_edit_ok": "Dépense mise à jour avec succès."},
    "it": {"btn_editar": "✏️ Modifica", "tit_editar": "Modifica Spesa", "msg_edit_ok": "Spesa aggiornata con successo."},
    "de": {"btn_editar": "✏️ Bearbeiten", "tit_editar": "Ausgabe Bearbeiten", "msg_edit_ok": "Ausgabe erfolgreich aktualisiert."}
}
for lang, dic in nuevos_textos_editar.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 13: GASTOS RECURRENTES AUTOMÁTICOS ---
if "gastos_recurrentes" not in CONFIG:
    CONFIG["gastos_recurrentes"] = []

nuevos_textos_recurrentes = {
    "es": {"menu_rec": "Gastos Recurrentes", "tit_rec": "Suscripciones y Pagos Fijos", "lbl_dia_cobro": "Día del mes (1-31):", "msg_rec_ok": "Suscripción agregada.", "msg_rec_del": "Suscripción eliminada.", "lbl_rec_act": "Tus pagos automáticos:", "txt_rec_marcador": "(Auto)"},
    "en": {"menu_rec": "Recurring Expenses", "tit_rec": "Subscriptions & Fixed Payments", "lbl_dia_cobro": "Day of month (1-31):", "msg_rec_ok": "Subscription added.", "msg_rec_del": "Subscription deleted.", "lbl_rec_act": "Your automatic payments:", "txt_rec_marcador": "(Auto)"},
    "pt": {"menu_rec": "Despesas Recorrentes", "tit_rec": "Assinaturas e Pagamentos", "lbl_dia_cobro": "Dia do mês (1-31):", "msg_rec_ok": "Assinatura adicionada.", "msg_rec_del": "Assinatura excluída.", "lbl_rec_act": "Seus pagamentos automáticos:", "txt_rec_marcador": "(Auto)"},
    "fr": {"menu_rec": "Dépenses Récurrentes", "tit_rec": "Abonnements et Paiements", "lbl_dia_cobro": "Jour du mois (1-31):", "msg_rec_ok": "Abonnement ajouté.", "msg_rec_del": "Abonnement supprimé.", "lbl_rec_act": "Vos paiements automatiques:", "txt_rec_marcador": "(Auto)"},
    "it": {"menu_rec": "Spese Ricorrenti", "tit_rec": "Abbonamenti e Pagamenti Fissi", "lbl_dia_cobro": "Giorno del mese (1-31):", "msg_rec_ok": "Abbonamento aggiunto.", "msg_rec_del": "Abbonamento eliminato.", "lbl_rec_act": "I tuoi pagamenti automatici:", "txt_rec_marcador": "(Auto)"},
    "de": {"menu_rec": "Wiederkehrende Ausgaben", "tit_rec": "Abonnements & Feste Zahlungen", "lbl_dia_cobro": "Tag des Monats (1-31):", "msg_rec_ok": "Abonnement hinzugefügt.", "msg_rec_del": "Abonnement gelöscht.", "lbl_rec_act": "Ihre automatischen Zahlungen:", "txt_rec_marcador": "(Auto)"}
}
for lang, dic in nuevos_textos_recurrentes.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 14: COMPROBANTES ---
nuevos_textos_adjuntos = {
    "es": {"btn_adjuntar": "📎 Adjuntar", "lbl_sin_archivo": "Sin archivo", "btn_ver_comp": "📎 Ver", "err_comp": "No se pudo abrir el archivo."},
    "en": {"btn_adjuntar": "📎 Attach", "lbl_sin_archivo": "No file", "btn_ver_comp": "📎 View", "err_comp": "Could not open file."},
    "pt": {"btn_adjuntar": "📎 Anexar", "lbl_sin_archivo": "Nenhum arquivo", "btn_ver_comp": "📎 Ver", "err_comp": "Não foi possível abrir o arquivo."},
    "fr": {"btn_adjuntar": "📎 Joindre", "lbl_sin_archivo": "Aucun fichier", "btn_ver_comp": "📎 Voir", "err_comp": "Impossible d'ouvrir le fichier."},
    "it": {"btn_adjuntar": "📎 Allega", "lbl_sin_archivo": "Nessun file", "btn_ver_comp": "📎 Vedi", "err_comp": "Impossibile aprire il file."},
    "de": {"btn_adjuntar": "📎 Anhängen", "lbl_sin_archivo": "Keine Datei", "btn_ver_comp": "📎 Ansehen", "err_comp": "Datei konnte nicht geöffnet werden."}
}
for lang, dic in nuevos_textos_adjuntos.items():
    if lang in TEXTOS: TEXTOS[lang].update(dic)

# --- INYECTOR 15: COMPARACIÓN INTELIGENTE ---
nuevos_textos_comparar = {
    "es": {"menu_comparar": "Comparar Períodos", "tit_comparar": "Comparación Inteligente", "lbl_mes1": "Período Base:", "lbl_mes2": "Período a Comparar:", "btn_comparar": "Analizar", "txt_dif": "Diferencia:", "txt_mas": "Gastaste {} MÁS ({}%)", "txt_menos": "Ahorraste {} ({}%)", "txt_igual": "Gastaste exactamente lo mismo.", "txt_sin_datos": "Necesitas al menos 2 meses de datos\npara poder comparar."},
    "en": {"menu_comparar": "Compare Periods", "tit_comparar": "Smart Comparison", "lbl_mes1": "Base Period:", "lbl_mes2": "Compare with:", "btn_comparar": "Analyze", "txt_dif": "Difference:", "txt_mas": "You spent {} MORE ({}%)", "txt_menos": "You saved {} ({}%)", "txt_igual": "You spent exactly the same.", "txt_sin_datos": "You need at least 2 months of data\nto compare."},
    "pt": {"menu_comparar": "Comparar Períodos", "tit_comparar": "Comparação Inteligente", "lbl_mes1": "Período Base:", "lbl_mes2": "Comparar com:", "btn_comparar": "Analisar", "txt_dif": "Diferença:", "txt_mas": "Você gastou {} A MAIS ({}%)", "txt_menos": "Você economizou {} ({}%)", "txt_igual": "Você gastou exatamente o mesmo.", "txt_sin_datos": "Você precisa de pelo menos 2 meses\nde dados para comparar."},
    "fr": {"menu_comparar": "Comparer Périodes", "tit_comparar": "Comparaison Intelligente", "lbl_mes1": "Période de Base:", "lbl_mes2": "Comparer avec:", "btn_comparar": "Analyser", "txt_dif": "Différence:", "txt_mas": "Vous avez dépensé {} DE PLUS ({}%)", "txt_menos": "Vous avez économisé {} ({}%)", "txt_igual": "Vous avez dépensé exactement pareil.", "txt_sin_datos": "Il faut au moins 2 mois de données\npour comparer."},
    "it": {"menu_comparar": "Confronta Periodi", "tit_comparar": "Confronto Intelligente", "lbl_mes1": "Periodo Base:", "lbl_mes2": "Confronta con:", "btn_comparar": "Analizza", "txt_dif": "Differenza:", "txt_mas": "Hai speso {} IN PIÙ ({}%)", "txt_menos": "Hai risparmiato {} ({}%)", "txt_igual": "Hai speso esattamente lo stesso.", "txt_sin_datos": "Hai bisogno di almeno 2 mesi di dati\nper confrontare."},
    "de": {"menu_comparar": "Zeiträume Vergleichen", "tit_comparar": "Intelligenter Vergleich", "lbl_mes1": "Basiszeitraum:", "lbl_mes2": "Vergleichen mit:", "btn_comparar": "Analysieren", "txt_dif": "Differenz:", "txt_mas": "Sie haben {} MEHR ausgegeben ({}%)", "txt_menos": "Sie haben {} gespart ({}%)", "txt_igual": "Sie haben genau gleich viel ausgegeben.", "txt_sin_datos": "Sie benötigen mindestens 2 Monate\nDaten zum Vergleichen."}
}
for lang, dic in nuevos_textos_comparar.items():
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
                        if len(partes) >= 4:
                            comp = partes[4].strip() if len(partes) > 4 else ""
                            gastos.append({"fecha": partes[0], "monto": int(partes[1]), "categoria": partes[2], "descripcion": partes[3], "comprobante": comp})
                except ValueError:
                    pass
    return ingreso, gastos

def guardar_datos(ingreso, gastos):
    archivo = obtener_ruta_archivo()
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(f"{ingreso}\n")
        for gasto in gastos:
            comp = gasto.get("comprobante", "")
            f.write(f"{gasto['fecha']}|{gasto['monto']}|{gasto['categoria']}|{gasto['descripcion']}|{comp}\n")

ruta_comprobante_actual = ""

def seleccionar_comprobante():
    global ruta_comprobante_actual
    ruta = filedialog.askopenfilename(title="Seleccionar Comprobante", filetypes=[("Imágenes y PDF", "*.png;*.jpg;*.jpeg;*.pdf")])
    if ruta:
        ruta_comprobante_actual = ruta
        nombre_corto = Path(ruta).name
        if len(nombre_corto) > 18: nombre_corto = nombre_corto[:15] + "..."
        lbl_archivo.configure(text=nombre_corto)

def abrir_archivo(nombre_archivo):
    ruta_absoluta = Path(CONFIG["ruta_datos"]) / "comprobantes" / nombre_archivo
    if not ruta_absoluta.exists():
        mostrar_alerta("error", "Error", t("err_comp"))
        return
    try:
        if sys.platform == "win32":
            os.startfile(ruta_absoluta)
        elif sys.platform == "darwin":
            subprocess.call(["open", str(ruta_absoluta)])
        else:
            subprocess.call(["xdg-open", str(ruta_absoluta)])
    except Exception as e:
        mostrar_alerta("error", "Error", f"{t('err_comp')} {e}")

def obtener_meses_disponibles():
    meses = set(gasto["fecha"][:7] for gasto in gastos_actuales)
    meses.add(datetime.now().strftime("%Y-%m"))
    return sorted(list(meses), reverse=True)

def obtener_gastos_del_mes(mes_seleccionado):
    return [g for g in gastos_actuales if g["fecha"].startswith(mes_seleccionado)]

# --- 4. INTERFAZ Y ACTUALIZACIONES ---
def aplicar_textos_ui():
    global ruta_comprobante_actual
    try:
        app.title(t("titulo"))
        titulo_form.configure(text=t("reg_gasto"))
        entrada_monto.configure(placeholder_text=t("ph_monto"))
        entrada_desc.configure(placeholder_text=t("ph_desc"))
        btn_guardar.configure(text=t("btn_guardar"))
        btn_buscar.configure(text=t("btn_buscar"))
        
        # --- NUEVO: TRADUCCIÓN DEL BOTÓN ADJUNTAR ---
        btn_adjuntar.configure(text=t("btn_adjuntar"))
        if not ruta_comprobante_actual:
            lbl_archivo.configure(text=t("lbl_sin_archivo"))
        # ---------------------------------------------
        
        # --- MAGIA MULTI-IDIOMA PARA EL COMBOBOX ---
        valor_antiguo = combo_categoria.get()
        clave_encontrada = None
        # Buscamos de qué clave interna venía ese texto (en cualquier idioma)
        for lang, dic in TEXTOS.items():
            for k, v in dic.items():
                if v == valor_antiguo and k.startswith("cat_"):
                    clave_encontrada = k
                    break
            if clave_encontrada: break
            
        categorias_base = [t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")]
        categorias_totales = categorias_base + CONFIG.get("categorias_custom", [])
        combo_categoria.configure(values=categorias_totales)
        
        # Le devolvemos su valor pero en el NUEVO idioma
        if clave_encontrada:
            combo_categoria.set(t(clave_encontrada))
        else:
            combo_categoria.set(categorias_base[0])

        # Opciones clásicas + Opción para ver todo
        opciones_basicas = [t("per_hoy"), t("per_sem"), t("per_mes"), t("per_6m"), t("per_ano"), t("opt_todas")]
        
        # Agregamos el historial de meses dinámicamente y traducidos
        meses_hist = obtener_meses_disponibles()
        idioma_act = CONFIG["idioma"]
        opciones_historicas = []
        for m_str in meses_hist: 
            y, m = m_str.split("-")
            nombre_mes = MESES[idioma_act].get(m, m)
            opciones_historicas.append(f"{nombre_mes} {y}")
            
        todas_opciones = opciones_basicas + opciones_historicas
        combo_periodos.configure(values=todas_opciones)
        
        valor_actual = combo_periodos.get()
        if not valor_actual or valor_actual not in todas_opciones:
            combo_periodos.set(t("per_mes"))
            
        actualizar_pantalla()
        
    except Exception as e:
        print(f"Pifia menor en la interfaz ignorada: {e}")

def obtener_cat_traducida_global(cat_guardada):
    clave_gasto = None
    for l, d in TEXTOS.items():
        for k, v in d.items():
            if v == cat_guardada and k.startswith("cat_"):
                clave_gasto = k
                break
        if clave_gasto: break
    return t(clave_gasto) if clave_gasto else cat_guardada

def dibujar_grafico(gastos_mes):
    global widget_grafico
    if widget_grafico is not None:
        widget_grafico.destroy()
    if not gastos_mes:
        return 

    totales_por_categoria = {}
    for gasto in gastos_mes:
        # MAGIA: Traducimos la categoría ANTES de sumarla. 
        # Así "Food" y "Comida" se suman en la misma barra.
        cat_trad = obtener_cat_traducida_global(gasto["categoria"])
        totales_por_categoria[cat_trad] = totales_por_categoria.get(cat_trad, 0) + gasto["monto"]

    totales_ordenados = sorted(totales_por_categoria.items(), key=lambda x: x[1])

    etiquetas = []
    valores = []
    for cat_trad, monto in totales_ordenados:
        etiquetas.append(cat_trad) # Ya viene traducida al idioma actual
        valores.append(monto)

    color_fondo = '#2B2B2B' if CONFIG["tema"] == "Oscuro" else '#EBEBEB'
    color_texto = 'white' if CONFIG["tema"] == "Oscuro" else 'black'
    color_barra = '#3498DB' 

    fig, ax = plt.subplots(figsize=(4, 2.5), facecolor=color_fondo)

    barras = ax.barh(etiquetas, valores, color=color_barra, height=0.6)

    ax.set_facecolor(color_fondo)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_visible(False) 
    ax.tick_params(axis='y', colors=color_texto, length=0, labelsize=10) 

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
        periodo_sel = combo_periodos.get()
    except:
        periodo_sel = t("per_mes") 
        
    hoy = datetime.now()
    gastos_filtrados = []
    
    mes_buscado_iso = None
    idioma_act = CONFIG["idioma"]
    for yyyy_mm in obtener_meses_disponibles():
        y, m = yyyy_mm.split("-")
        nombre_mes = MESES[idioma_act].get(m, m)
        if periodo_sel == f"{nombre_mes} {y}":
            mes_buscado_iso = yyyy_mm
            break
    
    for g in gastos_actuales:
        try:
            fecha_g = datetime.strptime(g["fecha"], "%Y-%m-%d")
        except: continue
            
        if periodo_sel == t("opt_todas"):
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_hoy") and fecha_g.date() == hoy.date():
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_sem") and (hoy - fecha_g).days <= 7:
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_mes") and fecha_g.month == hoy.month and fecha_g.year == hoy.year:
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_6m") and (hoy - fecha_g).days <= 180:
            gastos_filtrados.append(g)
        elif periodo_sel == t("per_ano") and fecha_g.year == hoy.year:
            gastos_filtrados.append(g)
        elif mes_buscado_iso and g["fecha"].startswith(mes_buscado_iso):
            gastos_filtrados.append(g)
            
    return gastos_filtrados

def actualizar_pantalla(*args):
    gastos_mes = obtener_gastos_por_periodo()
    
    periodo_texto = combo_periodos.get().upper() if combo_periodos.get() else "RESUMEN"
    lbl_dash_mes.configure(text=f"📊 {periodo_texto}")
    total_gastado = sum(g["monto"] for g in gastos_mes)
    plata_restante = ingreso_actual - total_gastado
    pct_gasto = (total_gastado / ingreso_actual) * 100 if ingreso_actual > 0 else 0

    mon = CONFIG["moneda"]
    lbl_dash_ingresos.configure(text=f"{t('dash_ingresos')} {mon}{ingreso_actual:,}".replace(",", "."))
    lbl_dash_gastos.configure(text=f"{t('dash_gastos')} {mon}{total_gastado:,}".replace(",", "."))
    lbl_dash_disponible.configure(text=f"{t('dash_disp')} {mon}{plata_restante:,}".replace(",", "."))
    lbl_dash_porcentaje.configure(text=t("dash_pct").format(f"{pct_gasto:.1f}".replace(".", ",")))
    lbl_titulo_historial.configure(text="📝 " + t("tit_movs"))

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

    # --- DIBUJAR HISTORIAL INTERACTIVO ---
    for widget in scroll_historial.winfo_children():
        widget.destroy()

    if not gastos_mes:
        ctk.CTkLabel(scroll_historial, text=t("sin_movs"), font=("Arial", 14, "italic")).pack(pady=20)
    else:
        for i, gasto in enumerate(gastos_mes, 1):
            monto_fmt = f"{gasto['monto']:,}".replace(",", ".")
            cat_trad = obtener_cat_traducida_global(gasto['categoria'])
            texto_item = f"[{gasto['fecha']}] {cat_trad}: {mon}{monto_fmt} - {gasto['descripcion']}"

            fila = ctk.CTkFrame(scroll_historial, fg_color="transparent")
            fila.pack(fill="x", pady=2)

            lbl = ctk.CTkLabel(fila, text=texto_item, font=("Arial", 14), anchor="w")
            lbl.pack(side="left", fill="x", expand=True)

            if gasto.get("comprobante"):
                btn_ver = ctk.CTkButton(fila, text=t("btn_ver_comp"), width=50, height=24, fg_color="#2980B9", hover_color="#1F618D", 
                                        command=lambda r=gasto["comprobante"]: abrir_archivo(r))
                btn_ver.pack(side="right", padx=5)

    dibujar_grafico(gastos_mes)

def verificar_primera_vez():
    global ingreso_actual
    hoy = datetime.now()
    dia_pago = CONFIG.get("dia_pago", 1)
    
    if hoy.day >= dia_pago:
        ciclo_actual = f"{hoy.year}-{hoy.month:02d}"
    else:
        mes_ant = hoy.month - 1 if hoy.month > 1 else 12
        anio_ant = hoy.year if hoy.month > 1 else hoy.year - 1
        ciclo_actual = f"{anio_ant}-{mes_ant:02d}"
        
    ciclo_guardado = CONFIG.get("ultimo_ciclo", "")

    if ingreso_actual <= 0 or ciclo_actual != ciclo_guardado:
        dialog = ctk.CTkInputDialog(text=f"{t('msg_ciclo_1')}{ciclo_actual}{t('msg_ciclo_2')}", title=t("tit_presupuesto"))
        respuesta = dialog.get_input()
        
        if respuesta and respuesta.replace(".", "").isdigit():
            ingreso_actual = int(respuesta.replace(".", ""))
            CONFIG["ultimo_ciclo"] = ciclo_actual
            guardar_config()
            guardar_datos(ingreso_actual, gastos_actuales) 
            actualizar_pantalla()
        elif ingreso_actual <= 0:
            ingreso_actual = 1
            guardar_datos(ingreso_actual, gastos_actuales)
            actualizar_pantalla()
            
    # --- AQUÍ DESPERTAMOS AL FANTASMA RECURRENTE ---
    procesar_gastos_recurrentes()

def resetear_datos_gui():
    resp = messagebox.askyesno(t("aj_peligro"), t("msg_reset_seguro"))
    if resp:
        global ingreso_actual
        gastos_actuales.clear()  
        ingreso_actual = 0       
        guardar_datos(ingreso_actual, gastos_actuales)
        
        CONFIG["ultimo_ciclo"] = ""
        guardar_config()
        
        mostrar_alerta("info", t("tit_reinicio"), t("msg_reinicio"))
        app.destroy() 

def guardar_gasto_gui():
    global ruta_comprobante_actual
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

    clave_real = None
    for lang, dic in TEXTOS.items():
        for k, v in dic.items():
            if v == categoria and k.startswith("cat_"):
                clave_real = k
                break
        if clave_real: break
        
    if not clave_real:
        clave_real = categoria

    limite = CONFIG.get("presupuestos_cat", {}).get(clave_real, 0)
    
    if limite > 0: 
        mes_actual_str = datetime.now().strftime("%Y-%m")
        gastos_mes_cat = 0
        for g in gastos_actuales:
            if g["fecha"].startswith(mes_actual_str):
                clave_gasto = None
                for l, d in TEXTOS.items():
                    for k, v in d.items():
                        if v == g["categoria"] and k.startswith("cat_"):
                            clave_gasto = k
                            break
                    if clave_gasto: break
                
                if clave_gasto == clave_real:
                    gastos_mes_cat += g["monto"]
        
        if gastos_mes_cat + monto > limite:
            mon = CONFIG["moneda"]
            mensaje = f"{t('txt_superado')} {categoria}!\n\nLímite: {mon}{limite:,}\nYa llevas: {mon}{gastos_mes_cat:,}\n+ Este gasto: {mon}{monto:,}\n\n{t('txt_guardar_igual')}"
            
            resp = messagebox.askyesno(t("msg_limite"), mensaje.replace(",", "."))
            if not resp:
                return 

    # --- GUARDADO SEGURO DE COMPROBANTE ---
    nombre_comprobante = ""
    if ruta_comprobante_actual:
        carpeta_comp = Path(CONFIG["ruta_datos"]) / "comprobantes"
        carpeta_comp.mkdir(parents=True, exist_ok=True)
        ext = Path(ruta_comprobante_actual).suffix
        nombre_comprobante = f"comp_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
        shutil.copy(ruta_comprobante_actual, carpeta_comp / nombre_comprobante)
        
        ruta_comprobante_actual = ""
        lbl_archivo.configure(text=t("lbl_sin_archivo"))

    gastos_actuales.append({
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "monto": monto,
        "categoria": categoria, 
        "descripcion": descripcion,
        "comprobante": nombre_comprobante
    })
    
    guardar_datos(ingreso_actual, gastos_actuales)
    actualizar_pantalla()

    entrada_monto.delete(0, "end")
    entrada_desc.delete(0, "end")

def exportar_datos(formato):
    if not gastos_actuales:
        mostrar_alerta("warning", t("alerta_cuidado"), t("sin_movs"))
        return
        
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    if formato == "csv":
        tipos = [(t("exp_csv"), "*.csv")]
        ext = ".csv"
    elif formato == "excel":
        tipos = [(t("exp_excel"), "*.xlsx")]
        ext = ".xlsx"
    else:
        tipos = [(t("exp_txt"), "*.txt")]
        ext = ".txt"

    ruta_guardado = filedialog.asksaveasfilename(
        title=t("menu_exportar"), 
        defaultextension=ext, 
        filetypes=tipos,
        initialfile=f"Mis_Gastos_{fecha_hoy}{ext}"
    )
    
    if not ruta_guardado:
        return 
        
    try:
        mon = CONFIG["moneda"]
        # Cargamos los títulos de las columnas en el idioma correcto
        encabezados = [t("col_fecha"), t("col_cat"), t("col_monto"), t("col_desc")]
        
        # --- TRADUCTOR UNIVERSAL DE CATEGORÍAS ---
        def obtener_cat_traducida(cat_guardada):
            clave_gasto = None
            for l, d in TEXTOS.items():
                for k, v in d.items():
                    if v == cat_guardada and k.startswith("cat_"):
                        clave_gasto = k
                        break
                if clave_gasto: break
            return t(clave_gasto) if clave_gasto else cat_guardada
        
        if formato == "txt":
            with open(ruta_guardado, "w", encoding="utf-8") as f:
                f.write(f"--- {t('titulo')} ---\n")
                f.write(f"{t('dash_ingresos')} {mon}{ingreso_actual}\n")
                f.write("-" * 40 + "\n")
                for g in gastos_actuales:
                    cat_trad = obtener_cat_traducida(g["categoria"])
                    f.write(f"[{g['fecha']}] {cat_trad} | {mon}{g['monto']} | {g['descripcion']}\n")
                    
        elif formato == "csv":
            with open(ruta_guardado, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(encabezados) # Escribe "Fecha", "Date", "Datum", etc.
                for g in gastos_actuales:
                    cat_trad = obtener_cat_traducida(g["categoria"])
                    writer.writerow([g['fecha'], cat_trad, g['monto'], g['descripcion']])
                    
        elif formato == "excel":
            try:
                import openpyxl
                from openpyxl.styles import Font
                wb = openpyxl.Workbook()
                ws = wb.active
                # Título de la hojita de Excel (máx 31 caracteres)
                ws.title = t("titulo")[:31] 
                
                # Escribimos los encabezados traducidos y en negrita
                ws.append(encabezados)
                for cell in ws["1:1"]:
                    cell.font = Font(bold=True)
                    
                for g in gastos_actuales:
                    cat_trad = obtener_cat_traducida(g["categoria"])
                    ws.append([g['fecha'], cat_trad, g['monto'], g['descripcion']])
                    
                wb.save(ruta_guardado)
            except ImportError:
                mostrar_alerta("error", "Falta Librería", t("err_excel"))
                return
                
        mostrar_alerta("info", t("alerta_listo"), f"{t('msg_exp_ok')}{ruta_guardado}")
        
    except Exception as e:
        mostrar_alerta("error", "Error", f"{t('msg_exp_err')}{e}")

def crear_backup():
    if not gastos_actuales and ingreso_actual == 0:
        mostrar_alerta("warning", t("alerta_cuidado"), t("sin_movs"))
        return
        
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    ruta_guardado = filedialog.asksaveasfilename(
        title=t("tit_backup"), 
        defaultextension=".json", 
        filetypes=[("JSON Backup", "*.json")],
        initialfile=f"backup_gastos_{fecha_hoy}.json"
    )
    
    if not ruta_guardado:
        return
        
    try:
        # Metemos todo en una cápsula
        datos_backup = {
            "ingreso_actual": ingreso_actual,
            "gastos_actuales": gastos_actuales
        }
        with open(ruta_guardado, "w", encoding="utf-8") as f:
            json.dump(datos_backup, f, indent=4)
            
        mostrar_alerta("info", t("alerta_listo"), f"{t('msg_backup_ok')}{ruta_guardado}")
    except Exception as e:
        mostrar_alerta("error", "Error", f"{t('err_general')}{e}")

def restaurar_backup():
    ruta_archivo = filedialog.askopenfilename(
        title=t("tit_restaurar"),
        filetypes=[("JSON Backup", "*.json")]
    )
    
    if not ruta_archivo:
        return
        
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos_backup = json.load(f)
            
        # Verificamos que sea un backup nuestro y no cualquier otro archivo JSON
        if "ingreso_actual" in datos_backup and "gastos_actuales" in datos_backup:
            global ingreso_actual
            
            # Pregunta de seguridad antes de pisar los datos
            resp = messagebox.askyesno(t("alerta_cuidado"), t("msg_conf_restaurar"))
            if not resp:
                return
                
            # Sobrescribimos la memoria de la app
            ingreso_actual = datos_backup["ingreso_actual"]
            gastos_actuales.clear()
            gastos_actuales.extend(datos_backup["gastos_actuales"])
            
            # Guardamos a fuego en el disco duro y recargamos pantalla
            guardar_datos(ingreso_actual, gastos_actuales)
            actualizar_pantalla()
            
            mostrar_alerta("info", t("alerta_listo"), t("msg_restaurar_ok"))
        else:
            mostrar_alerta("error", "Error", t("err_backup_leer"))
            
    except Exception as e:
        mostrar_alerta("error", "Error", f"{t('err_general')}{e}")

def mostrar_acerca_de_gui():
    texto_about = f"{t('titulo')} V1.0\n\nDev: Mathias\nIngeniería Informática\nUniversidad de Valparaíso"
    mostrar_alerta("info", t("btn_acerca"), texto_about)

def agregar_categoria_gui():
    dialog = ctk.CTkInputDialog(text=t("msg_add_cat"), title=t("tit_add_cat"))
    nueva_cat = dialog.get_input()
    
    if nueva_cat is not None:
        nueva_cat = nueva_cat.strip()
        if not nueva_cat:
            mostrar_alerta("warning", "Error", t("err_cat_vacia"))
            return
            
        # Comparamos que no exista en las por defecto ni en las personalizadas
        cat_base = [t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")]
        if nueva_cat in cat_base or nueva_cat in CONFIG.get("categorias_custom", []):
            mostrar_alerta("warning", "Error", t("msg_cat_existe"))
            return
            
        # Si todo está bien, la guardamos y recargamos la pantalla
        CONFIG.setdefault("categorias_custom", []).append(nueva_cat)
        guardar_config()
        aplicar_textos_ui() # Refresca el combobox al instante
        mostrar_alerta("info", t("alerta_listo"), t("msg_cat_ok"))

def eliminar_categoria_gui():
    custom_cats = CONFIG.get("categorias_custom", [])
    if not custom_cats:
        mostrar_alerta("info", t("tit_del_cat"), t("msg_no_custom_cat"))
        return

    ventana_del = ctk.CTkToplevel(app)
    ventana_del.title(t("tit_del_cat"))
    ventana_del.geometry("350x200")
    ventana_del.attributes("-topmost", True)

    ctk.CTkLabel(ventana_del, text=t("lbl_sel_del_cat"), font=("Arial", 14)).pack(pady=(20, 10))

    combo_del = ctk.CTkComboBox(ventana_del, values=custom_cats, width=200)
    combo_del.set(custom_cats[0])
    combo_del.pack(pady=10)

    def confirmar_eliminar():
        cat_a_borrar = combo_del.get()
        if cat_a_borrar in custom_cats:
            # Preguntamos si está seguro e inyectamos el nombre de la categoría en el texto
            resp = messagebox.askyesno(t("aj_peligro"), t("msg_conf_del_cat").format(cat_a_borrar))
            if resp:
                # 1. La borramos de la lista
                CONFIG["categorias_custom"].remove(cat_a_borrar)
                
                # 2. Le borramos su presupuesto si es que le había asignado uno
                if cat_a_borrar in CONFIG.get("presupuestos_cat", {}):
                    del CONFIG["presupuestos_cat"][cat_a_borrar]
                    
                # 3. Guardamos y refrescamos
                guardar_config()
                aplicar_textos_ui() 
                ventana_del.destroy()
                mostrar_alerta("info", t("alerta_listo"), t("msg_cat_del_ok"))

    btn_del = ctk.CTkButton(ventana_del, text=t("tit_del_cat"), fg_color="#C0392B", hover_color="#922B21", font=("Arial", 14, "bold"), command=confirmar_eliminar)
    btn_del.pack(pady=(10, 20))

def abrir_ventana_limites():
    ventana_limites = ctk.CTkToplevel(app)
    ventana_limites.title(t("btn_limites"))
    ventana_limites.geometry("400x500")
    ventana_limites.attributes("-topmost", True)

    lbl_tit = ctk.CTkLabel(ventana_limites, text=t("tit_limites"), font=("Arial", 16, "bold"))
    lbl_tit.pack(pady=15)

    # AHORA ES UN SCROLLABLE FRAME POR SI EL USUARIO CREA 100 CATEGORÍAS
    frame_entradas = ctk.CTkScrollableFrame(ventana_limites, fg_color="transparent")
    frame_entradas.pack(fill="both", expand=True, padx=20)

    lista_categorias_claves = ["cat_comida", "cat_juegos", "cat_transporte", "cat_servicios", "cat_hogar", "cat_otros"]
    entradas = {}
    fila_actual = 0

    # 1. Cargamos las categorías predeterminadas
    for clave in lista_categorias_claves:
        ctk.CTkLabel(frame_entradas, text=t(clave), font=("Arial", 14)).grid(row=fila_actual, column=0, sticky="w", pady=10)
        ent = ctk.CTkEntry(frame_entradas, width=150, justify="right")
        ent.insert(0, str(CONFIG["presupuestos_cat"].get(clave, 0)))
        ent.grid(row=fila_actual, column=1, sticky="e", pady=10, padx=10)
        entradas[clave] = ent
        fila_actual += 1
        
    # 2. Cargamos las categorías personalizadas del usuario
    for cat_custom in CONFIG.get("categorias_custom", []):
        ctk.CTkLabel(frame_entradas, text=cat_custom, font=("Arial", 14)).grid(row=fila_actual, column=0, sticky="w", pady=10)
        ent = ctk.CTkEntry(frame_entradas, width=150, justify="right")
        ent.insert(0, str(CONFIG["presupuestos_cat"].get(cat_custom, 0)))
        ent.grid(row=fila_actual, column=1, sticky="e", pady=10, padx=10)
        entradas[cat_custom] = ent
        fila_actual += 1

    def guardar_limites():
        limites_temp = {}
        suma_total = 0
        for clave, ent in entradas.items():
            valor_str = ent.get().replace(".", "").strip()
            try:
                valor = int(valor_str) if valor_str.isdigit() else 0
            except:
                valor = 0
            limites_temp[clave] = valor
            suma_total += valor
            
        if suma_total > ingreso_actual:
            mon = CONFIG.get("moneda", "$")
            suma_fmt = f"{suma_total:,}".replace(",", ".")
            ingreso_fmt = f"{ingreso_actual:,}".replace(",", ".")
            texto_alerta = f"{t('msg_pres_exc_1')}{mon}{suma_fmt}{t('msg_pres_exc_2')}{mon}{ingreso_fmt}{t('msg_pres_exc_3')}"
            mostrar_alerta("warning", t("tit_pres_exc"), texto_alerta)
            return 
            
        CONFIG["presupuestos_cat"] = limites_temp
        guardar_config()
        ventana_limites.destroy()
        mostrar_alerta("info", t("alerta_listo"), t("msg_limites_ok"))

    def limpiar_a_cero():
        for ent in entradas.values():
            ent.delete(0, "end")
            ent.insert(0, "0")

    btn_limpiar = ctk.CTkButton(ventana_limites, text=t("btn_limpiar_0"), command=limpiar_a_cero, fg_color="#7F8C8D", hover_color="#616A6B", font=("Arial", 14))
    btn_limpiar.pack(pady=(10, 5), fill="x", padx=20)

    btn_guardar_lim = ctk.CTkButton(ventana_limites, text=t("btn_guardar_lim_2"), command=guardar_limites, fg_color="#E67E22", hover_color="#D35400", font=("Arial", 14, "bold"))
    btn_guardar_lim.pack(pady=(5, 20), fill="x", padx=20)

def configurar_dia_pago():
    dia_actual = CONFIG.get("dia_pago", 1)
    dialog = ctk.CTkInputDialog(text=f"{t('msg_dia_pago_1')}{dia_actual}{t('msg_dia_pago_2')}", title=t("tit_dia_pago"))
    respuesta = dialog.get_input()
    
    if respuesta and respuesta.isdigit():
        dia = int(respuesta)
        if 1 <= dia <= 31:
            CONFIG["dia_pago"] = dia
            guardar_config()
            mostrar_alerta("info", t("tit_dia_act"), f"{t('msg_dia_ok_1')}{dia}{t('msg_dia_ok_2')}")
            verificar_primera_vez() 
        else:
            mostrar_alerta("warning", "Error", t("err_dia"))

def abrir_edicion_gasto(gasto_a_editar, ventana_busqueda_padre):
    # Buscamos el índice real del gasto en la lista global para poder sobrescribirlo
    try:
        indice_real = gastos_actuales.index(gasto_a_editar)
    except ValueError:
        mostrar_alerta("error", "Error", "No se encontró el gasto en la base de datos.")
        return
        
    gasto = gastos_actuales[indice_real]
    
    ventana_edit = ctk.CTkToplevel(app)
    ventana_edit.title(t("tit_editar"))
    ventana_edit.geometry("400x450")
    ventana_edit.attributes("-topmost", True)
    
    ctk.CTkLabel(ventana_edit, text=t("tit_editar"), font=("Arial", 16, "bold")).pack(pady=10)
    
    # 1. Fecha
    ctk.CTkLabel(ventana_edit, text=t("col_fecha")).pack(pady=(5, 0))
    ent_fecha = ctk.CTkEntry(ventana_edit, width=200)
    ent_fecha.insert(0, gasto["fecha"])
    ent_fecha.pack(pady=5)
    
    # 2. Monto
    ctk.CTkLabel(ventana_edit, text=t("col_monto")).pack(pady=(5, 0))
    ent_monto = ctk.CTkEntry(ventana_edit, width=200)
    ent_monto.insert(0, str(gasto["monto"]))
    ent_monto.pack(pady=5)
    
    # 3. Categoría (Con traductor inverso para mostrarla bien)
    ctk.CTkLabel(ventana_edit, text=t("col_cat")).pack(pady=(5, 0))
    categorias_disponibles = [t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")] + CONFIG.get("categorias_custom", [])
    
    cat_actual_traducida = gasto["categoria"]
    for l, d in TEXTOS.items():
        for k, v in d.items():
            if v == gasto["categoria"] and k.startswith("cat_"):
                cat_actual_traducida = t(k)
                break
                
    combo_cat = ctk.CTkComboBox(ventana_edit, values=categorias_disponibles, width=200)
    if cat_actual_traducida in categorias_disponibles:
        combo_cat.set(cat_actual_traducida)
    else:
        combo_cat.set(gasto["categoria"])
    combo_cat.pack(pady=5)
    
    # 4. Descripción
    ctk.CTkLabel(ventana_edit, text=t("col_desc")).pack(pady=(5, 0))
    ent_desc = ctk.CTkEntry(ventana_edit, width=200)
    ent_desc.insert(0, gasto["descripcion"])
    ent_desc.pack(pady=5)
    
    def guardar_cambios():
        monto_str = ent_monto.get().strip().replace(".", "")
        try:
            nuevo_monto = int(monto_str)
            if nuevo_monto <= 0: raise ValueError
        except ValueError:
            mostrar_alerta("warning", "Error", t("alerta_monto"))
            return
            
        # Sobrescribimos el gasto en la lista oficial
        gastos_actuales[indice_real]["monto"] = nuevo_monto
        gastos_actuales[indice_real]["categoria"] = combo_cat.get()
        gastos_actuales[indice_real]["descripcion"] = ent_desc.get().strip() or "..."
        gastos_actuales[indice_real]["fecha"] = ent_fecha.get().strip() or gasto["fecha"]
        
        guardar_datos(ingreso_actual, gastos_actuales)
        actualizar_pantalla()
        
        ventana_edit.destroy()
        # Destruimos la ventana de búsqueda para que el usuario la vuelva a abrir y se refresque la lista
        ventana_busqueda_padre.destroy() 
        mostrar_alerta("info", t("alerta_listo"), t("msg_edit_ok"))
        
    btn_guardar = ctk.CTkButton(ventana_edit, text=t("btn_guardar"), fg_color="#F39C12", hover_color="#D68910", font=("Arial", 14, "bold"), command=guardar_cambios)
    btn_guardar.pack(pady=20)

def procesar_gastos_recurrentes():
    hoy = datetime.now()
    mes_actual_str = hoy.strftime("%Y-%m")
    dia_hoy = hoy.day
    hubo_cambios = False
    
    for rec in CONFIG.get("gastos_recurrentes", []):
        # Revisa si en ESTE mes ya se pagó. Si no se ha pagado, evalúa si ya llegó el día de cobro.
        if rec.get("ultimo_mes") != mes_actual_str:
            if dia_hoy >= rec.get("dia", 1):
                # Generamos la fecha exacta del cobro (con seguro anti-febrero)
                try:
                    fecha_gasto = hoy.replace(day=rec.get("dia", 1)).strftime("%Y-%m-%d")
                except ValueError:
                    fecha_gasto = hoy.strftime("%Y-%m-%d") # Si es 31 y el mes trae 30, usa hoy
                
                gastos_actuales.append({
                    "fecha": fecha_gasto,
                    "monto": rec["monto"],
                    "categoria": rec["cat"],
                    "descripcion": f"{rec['desc']} {t('txt_rec_marcador')}"
                })
                # Le ponemos la firma de que ya se cobró este mes para no duplicarlo
                rec["ultimo_mes"] = mes_actual_str
                hubo_cambios = True
                
    if hubo_cambios:
        guardar_datos(ingreso_actual, gastos_actuales)
        guardar_config()
        actualizar_pantalla()

def abrir_ventana_recurrentes():
    vent_rec = ctk.CTkToplevel(app)
    vent_rec.title(t("tit_rec"))
    vent_rec.geometry("450x650")
    vent_rec.attributes("-topmost", True)

    ctk.CTkLabel(vent_rec, text="🔄 " + t("tit_rec"), font=("Arial", 18, "bold")).pack(pady=15)

    frame_add = ctk.CTkFrame(vent_rec)
    frame_add.pack(padx=20, fill="x")

    ent_desc = ctk.CTkEntry(frame_add, placeholder_text=t("col_desc") + " (ej: Spotify)")
    ent_desc.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    ent_monto = ctk.CTkEntry(frame_add, placeholder_text=t("col_monto") + " (ej: 6000)")
    ent_monto.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    categorias_disp = [t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")] + CONFIG.get("categorias_custom", [])
    combo_cat = ctk.CTkComboBox(frame_add, values=categorias_disp)
    combo_cat.set(t("cat_servicios"))
    combo_cat.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    ent_dia = ctk.CTkEntry(frame_add, placeholder_text=t("lbl_dia_cobro"))
    ent_dia.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    frame_add.grid_columnconfigure(0, weight=1)
    frame_add.grid_columnconfigure(1, weight=1)

    # Frame donde listaremos las suscripciones
    ctk.CTkLabel(vent_rec, text=t("lbl_rec_act"), font=("Arial", 14, "bold")).pack(pady=(20, 5), anchor="w", padx=20)
    scroll_rec = ctk.CTkScrollableFrame(vent_rec, fg_color="#1E1E1E")
    scroll_rec.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refrescar_lista():
        for widget in scroll_rec.winfo_children():
            widget.destroy()
            
        mon = CONFIG["moneda"]
        for idx, rec in enumerate(CONFIG.get("gastos_recurrentes", [])):
            fila = ctk.CTkFrame(scroll_rec, fg_color="transparent")
            fila.pack(fill="x", pady=5)
            
            # Buscamos su traducción
            cat_trad = rec["cat"]
            for l, d in TEXTOS.items():
                for k, v in d.items():
                    if v == rec["cat"] and k.startswith("cat_"):
                        cat_trad = t(k)
                        break

            monto_fmt = f"{rec['monto']:,}".replace(",", ".")
            texto = f"Día {rec['dia']} | {rec['desc']} | {cat_trad}: {mon}{monto_fmt}"
            
            ctk.CTkLabel(fila, text=texto, font=("Arial", 13)).pack(side="left", padx=5)
            btn_del = ctk.CTkButton(fila, text="🗑️", width=30, fg_color="#C0392B", hover_color="#922B21", 
                                    command=lambda i=idx: borrar_recurrente(i))
            btn_del.pack(side="right", padx=5)

    def borrar_recurrente(indice):
        CONFIG["gastos_recurrentes"].pop(indice)
        guardar_config()
        refrescar_lista()
        mostrar_alerta("info", "Info", t("msg_rec_del"))

    def guardar_recurrente():
        desc = ent_desc.get().strip()
        monto_str = ent_monto.get().strip().replace(".", "")
        dia_str = ent_dia.get().strip()
        cat = combo_cat.get()

        if not desc or not monto_str or not dia_str:
            mostrar_alerta("warning", "Error", "Completa todos los campos.")
            return

        try:
            monto = int(monto_str)
            dia = int(dia_str)
            if monto <= 0 or dia < 1 or dia > 31: raise ValueError
        except ValueError:
            mostrar_alerta("warning", "Error", "Ingresa un monto y un día (1-31) válidos.")
            return

        # Devolvemos la categoría a su forma original antes de guardar
        clave_real = None
        for lang, dic in TEXTOS.items():
            for k, v in dic.items():
                if v == cat and k.startswith("cat_"):
                    clave_real = k
                    break
            if clave_real: break
        cat_guardar = cat if not clave_real else TEXTOS["es"].get(clave_real, cat)

        nueva_suscripcion = {
            "desc": desc,
            "monto": monto,
            "cat": cat_guardar,
            "dia": dia,
            "ultimo_mes": "" # Vacío para que se cobre apenas corresponda
        }

        CONFIG["gastos_recurrentes"].append(nueva_suscripcion)
        guardar_config()
        ent_desc.delete(0, "end")
        ent_monto.delete(0, "end")
        ent_dia.delete(0, "end")
        
        # Procesamos de inmediato por si el día de cobro ya pasó este mes
        procesar_gastos_recurrentes() 
        refrescar_lista()
        mostrar_alerta("info", "Info", t("msg_rec_ok"))

    btn_guardar_rec = ctk.CTkButton(frame_add, text=t("btn_guardar"), fg_color="#27AE60", hover_color="#1E8449", font=("Arial", 14, "bold"), command=guardar_recurrente)
    btn_guardar_rec.grid(row=2, column=0, columnspan=2, pady=(15, 5))

    refrescar_lista()

def abrir_ventana_comparacion():
    vent_comp = ctk.CTkToplevel(app)
    vent_comp.title(t("tit_comparar"))
    vent_comp.geometry("450x450")
    vent_comp.attributes("-topmost", True)

    ctk.CTkLabel(vent_comp, text="📉 " + t("tit_comparar"), font=("Arial", 20, "bold")).pack(pady=20)

    meses_disp_iso = obtener_meses_disponibles()
    if len(meses_disp_iso) < 2:
        ctk.CTkLabel(vent_comp, text=t("txt_sin_datos"), font=("Arial", 14), text_color="#F39C12").pack(pady=40)
        return

    idioma_act = CONFIG["idioma"]
    meses_nombres = []
    nombre_a_iso = {}

    # Traducimos los meses para que se vean bonitos en el seleccionador
    for m_str in meses_disp_iso:
        y, m = m_str.split("-")
        nombre_mes = f"{MESES[idioma_act].get(m, m)} {y}"
        meses_nombres.append(nombre_mes)
        nombre_a_iso[nombre_mes] = m_str

    frame_sel = ctk.CTkFrame(vent_comp, fg_color="transparent")
    frame_sel.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(frame_sel, text=t("lbl_mes1"), font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=(0, 5))
    combo_mes1 = ctk.CTkComboBox(frame_sel, values=meses_nombres)
    # Por defecto selecciona el mes anterior
    combo_mes1.set(meses_nombres[1] if len(meses_nombres) > 1 else meses_nombres[0]) 
    combo_mes1.grid(row=1, column=0, sticky="ew", padx=(0, 10))

    ctk.CTkLabel(frame_sel, text=t("lbl_mes2"), font=("Arial", 12)).grid(row=0, column=1, sticky="w", pady=(0, 5))
    combo_mes2 = ctk.CTkComboBox(frame_sel, values=meses_nombres)
    # Por defecto selecciona el mes actual
    combo_mes2.set(meses_nombres[0]) 
    combo_mes2.grid(row=1, column=1, sticky="ew")

    frame_sel.grid_columnconfigure(0, weight=1)
    frame_sel.grid_columnconfigure(1, weight=1)

    frame_res = ctk.CTkFrame(vent_comp, fg_color="#1E1E1E")
    frame_res.pack(fill="both", expand=True, padx=20, pady=20)

    def calcular_comparacion():
        for widget in frame_res.winfo_children():
            widget.destroy()

        iso1 = nombre_a_iso[combo_mes1.get()]
        iso2 = nombre_a_iso[combo_mes2.get()]

        gastos_m1 = sum(g["monto"] for g in gastos_actuales if g["fecha"].startswith(iso1))
        gastos_m2 = sum(g["monto"] for g in gastos_actuales if g["fecha"].startswith(iso2))

        mon = CONFIG["moneda"]
        g1_fmt = f"{mon}{gastos_m1:,}".replace(",", ".")
        g2_fmt = f"{mon}{gastos_m2:,}".replace(",", ".")

        ctk.CTkLabel(frame_res, text=f"{combo_mes1.get()}:  {g1_fmt}", font=("Arial", 15)).pack(pady=(20, 5))
        ctk.CTkLabel(frame_res, text=f"{combo_mes2.get()}:  {g2_fmt}", font=("Arial", 15)).pack(pady=(5, 15))

        if gastos_m1 == 0 and gastos_m2 == 0:
            ctk.CTkLabel(frame_res, text=t("txt_igual"), font=("Arial", 16, "bold"), text_color="gray").pack()
            return

        diferencia = gastos_m2 - gastos_m1
        if gastos_m1 > 0:
            pct = (abs(diferencia) / gastos_m1) * 100
        else:
            pct = 100 # Si el mes base fue 0, creció desde la nada

        dif_fmt = f"{mon}{abs(diferencia):,}".replace(",", ".")
        pct_fmt = f"{pct:.1f}".replace(".", ",")

        if diferencia > 0:
            texto_final = t("txt_mas").format(dif_fmt, pct_fmt)
            color = "#E74C3C" # Rojo (gastó de más)
        elif diferencia < 0:
            texto_final = t("txt_menos").format(dif_fmt, pct_fmt)
            color = "#2ECC71" # Verde (ahorró)
        else:
            texto_final = t("txt_igual")
            color = "white" if CONFIG["tema"] == "Oscuro" else "black"

        ctk.CTkFrame(frame_res, height=2, fg_color="gray").pack(fill="x", padx=30, pady=5)
        ctk.CTkLabel(frame_res, text=texto_final, font=("Arial", 18, "bold"), text_color=color).pack(pady=15)

    btn_calc = ctk.CTkButton(vent_comp, text=t("btn_comparar"), fg_color="#2980B9", hover_color="#1F618D", command=calcular_comparacion, font=("Arial", 14, "bold"))
    btn_calc.pack(pady=(0, 20))
    
    # Lo ejecutamos de inmediato para mostrar el mes actual vs el anterior
    calcular_comparacion()

def abrir_ventana_buscar():
    ventana_buscar = ctk.CTkToplevel(app)
    ventana_buscar.title("🔍 " + t("tit_buscar"))
    ventana_buscar.geometry("750x600")
    ventana_buscar.attributes("-topmost", True)

    frame_filtros = ctk.CTkFrame(ventana_buscar)
    frame_filtros.pack(fill="x", padx=10, pady=10)

    scroll_resultados = ctk.CTkScrollableFrame(ventana_buscar, fg_color="#1E1E1E")
    scroll_resultados.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def borrar_desde_buscador(gasto_a_borrar):
        resp = messagebox.askyesno(t("aj_peligro"), f"{t('msg_borrar')}\n\n{gasto_a_borrar['descripcion']} - {CONFIG['moneda']}{gasto_a_borrar['monto']}")
        if resp:
            gastos_actuales.remove(gasto_a_borrar)
            guardar_datos(ingreso_actual, gastos_actuales)
            actualizar_pantalla() 
            aplicar_busqueda()    
            mostrar_alerta("info", t("alerta_listo"), t("alerta_borrado"))
            ventana_buscar.attributes("-topmost", True) 

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

        if orden_sel == t("ord_fecha_desc"): resultados.sort(key=lambda x: x["fecha"], reverse=True)
        elif orden_sel == t("ord_fecha_asc"): resultados.sort(key=lambda x: x["fecha"])
        elif orden_sel == t("ord_monto_desc"): resultados.sort(key=lambda x: x["monto"], reverse=True)
        elif orden_sel == t("ord_monto_asc"): resultados.sort(key=lambda x: x["monto"])

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
                
                fila = ctk.CTkFrame(scroll_resultados, fg_color="transparent")
                fila.pack(fill="x", pady=2, padx=5)
                
                texto_item = f"[{g['fecha']}] {cat_trad}: {mon}{monto_fmt} - {g['descripcion']}"
                lbl_texto = ctk.CTkLabel(fila, text=texto_item, font=("Arial", 14), anchor="w")
                lbl_texto.pack(side="left", fill="x", expand=True)
                
                btn_del = ctk.CTkButton(fila, text="🗑️", width=35, fg_color="#C0392B", hover_color="#922B21", 
                                        command=lambda gasto=g: borrar_desde_buscador(gasto))
                btn_del.pack(side="right")
                btn_editar = ctk.CTkButton(fila, text=t("btn_editar"), width=70, fg_color="#F39C12", hover_color="#D68910", 
                                        command=lambda gasto=g: abrir_edicion_gasto(gasto, ventana_buscar))
                btn_editar.pack(side="right", padx=5)
            
            total_fmt = f"{total_filtrado:,}".replace(",", ".")
            ctk.CTkFrame(scroll_resultados, height=2, fg_color="gray").pack(fill="x", pady=(15, 5))
            lbl_total = ctk.CTkLabel(scroll_resultados, text=f"{t('lbl_total_enc')} {mon}{total_fmt}", font=("Arial", 16, "bold"))
            lbl_total.pack(anchor="w", padx=5)

    ctk.CTkLabel(frame_filtros, text=t("lbl_busqueda")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ent_texto = ctk.CTkEntry(frame_filtros, width=200, placeholder_text="Ej: Steam, comida...")
    ent_texto.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(frame_filtros, text=t("lbl_monto_min")).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    ent_monto = ctk.CTkEntry(frame_filtros, width=150, placeholder_text="Ej: 10000")
    ent_monto.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    ctk.CTkLabel(frame_filtros, text=t("lbl_filtro_cat")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    cat_loc = [t("opt_todas"), t("cat_comida"), t("cat_juegos"), t("cat_transporte"), t("cat_servicios"), t("cat_hogar"), t("cat_otros")] + CONFIG.get("categorias_custom", [])
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

    btn_filtro = ctk.CTkButton(frame_filtros, text=f"🔍 {t('btn_aplicar_filtros').upper()}", fg_color="#2980B9", hover_color="#1F618D", font=("Arial", 14, "bold"), height=35, command=aplicar_busqueda)
    btn_filtro.grid(row=2, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

    ventana_buscar.bind('<Return>', aplicar_busqueda)
    aplicar_busqueda()

def restaurar_fabrica_gui():
    resp = messagebox.askyesno(t("aj_peligro"), t("msg_conf_fabrica"))
    if resp:
        if ARCHIVO_CONFIG.exists(): 
            ARCHIVO_CONFIG.unlink()
        mostrar_alerta("info", t("tit_reinicio_fab"), t("msg_reinicio_fab"))
        app.destroy()

# --- 5. ARRANQUE PRINCIPAL ---
cargar_config()
ingreso_actual, gastos_actuales = cargar_datos()

app = ctk.CTk()
app.geometry("1024x720")
app.minsize(900, 600)

def cerrar_programa():
    app.quit()    
    app.destroy() 

app.protocol("WM_DELETE_WINDOW", cerrar_programa)

app.grid_columnconfigure(0, weight=0) 
app.grid_columnconfigure(1, weight=1) 
app.grid_rowconfigure(0, weight=1)    

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
    construir_menu() 

def construir_menu():
    barra_menu.delete(0, "end") 
    
# 1. Archivo
    menu_archivo = tk.Menu(barra_menu, tearoff=0)
    
    # --- SUBMENÚ DE EXPORTACIÓN ---
    menu_exportar = tk.Menu(menu_archivo, tearoff=0)
    menu_exportar.add_command(label=t("exp_csv"), command=lambda: exportar_datos("csv"))
    menu_exportar.add_command(label=t("exp_excel"), command=lambda: exportar_datos("excel"))
    menu_exportar.add_command(label=t("exp_txt"), command=lambda: exportar_datos("txt"))
    
    menu_archivo.add_cascade(label=t("menu_exportar"), menu=menu_exportar)
    menu_archivo.add_separator() 
    
    # --- BACKUP Y RESTAURACIÓN ---
    menu_archivo.add_command(label=t("menu_backup"), command=crear_backup)
    menu_archivo.add_command(label=t("menu_restaurar"), command=restaurar_backup)
    menu_archivo.add_separator()
    
    # --- BOTÓN SALIR ÚNICO ---
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
    menu_herramientas.add_command(label=t("menu_add_cat"), command=agregar_categoria_gui)
    menu_herramientas.add_command(label=t("menu_del_cat"), command=eliminar_categoria_gui)
    menu_herramientas.add_command(label=t("menu_comparar"), command=abrir_ventana_comparacion)
    menu_herramientas.add_command(label=t("menu_rec"), command=abrir_ventana_recurrentes)
    menu_herramientas.add_command(label=t("menu_dia_pago"), command=configurar_dia_pago)
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

construir_menu()

# --- PANELES CON EL NUEVO SISTEMA GRID ---
frame_izquierdo = ctk.CTkFrame(app, width=320) 
frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
frame_izquierdo.grid_propagate(False) 

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

# --- NUEVO: BOTÓN ADJUNTAR ---
frame_adjunto = ctk.CTkFrame(frame_izquierdo, fg_color="transparent")
frame_adjunto.pack(pady=5, padx=20, fill="x")
btn_adjuntar = ctk.CTkButton(frame_adjunto, text="📎 Adjuntar", width=100, fg_color="#34495E", hover_color="#2C3E50", command=seleccionar_comprobante)
btn_adjuntar.pack(side="left", padx=(0, 10))
lbl_archivo = ctk.CTkLabel(frame_adjunto, text="Sin archivo", font=("Arial", 11), text_color="gray")
lbl_archivo.pack(side="left", fill="x", expand=True)

btn_guardar = ctk.CTkButton(frame_izquierdo, text="", command=guardar_gasto_gui, font=("Arial", 14, "bold"))
btn_guardar.pack(pady=(20, 10), padx=20, fill="x")

btn_buscar = ctk.CTkButton(frame_izquierdo, text="", command=abrir_ventana_buscar, fg_color="#8E44AD", hover_color="#732D91", font=("Arial", 12, "bold"))
btn_buscar.pack(pady=5, padx=20, fill="x")

# PANEL DERECHO
combo_periodos = ctk.CTkComboBox(frame_derecho, command=actualizar_pantalla, width=220, font=("Arial", 14), state="readonly")
combo_periodos.pack(pady=(20, 5), padx=20, anchor="e")

lbl_dash_mes = ctk.CTkLabel(frame_derecho, text="📊 RESUMEN", font=("Arial", 28, "bold"))
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

lbl_titulo_historial = ctk.CTkLabel(frame_derecho, text="📝 Movimientos", font=("Arial", 16, "bold"))
lbl_titulo_historial.pack(anchor="w", padx=20, pady=(20, 5))

scroll_historial = ctk.CTkScrollableFrame(frame_derecho, fg_color="#1E1E1E", height=180)
scroll_historial.pack(fill="both", expand=True, padx=20, pady=(0, 20))

construir_menu()
aplicar_textos_ui()
app.after(100, verificar_primera_vez)
app.mainloop()