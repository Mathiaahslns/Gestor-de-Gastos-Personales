# 📊 Gestor de Gastos Personales

Aplicación de escritorio avanzada para la gestión de finanzas personales, desarrollada íntegramente en Python. Diseñada con una interfaz moderna y responsiva, permite llevar un control total de tus movimientos financieros de forma local, segura y altamente personalizable.

## ✨ Características Principales (Killer Features)

- 🌍 **Soporte Multi-idioma Dinámico:** Disponible en 6 idiomas (Español, Inglés, Portugués, Francés, Italiano, Alemán) con cambio en tiempo real.
- 🔁 **Automatización de Gastos Recurrentes:** Configura pagos fijos (Spotify, Netflix, Arriendo) para que el sistema los cobre automáticamente el día que corresponde, evitando duplicados.
- 📉 **Comparación Inteligente:** Compara gráficamente y matemáticamente el rendimiento de dos meses distintos, mostrando variaciones exactas de dinero y porcentaje de ahorro/pérdida.
- 🧾 **Gestión de Comprobantes:** Adjunta boletas (imágenes) o facturas (PDF) a tus gastos. El sistema crea una bóveda segura local para que nunca pierdas un comprobante.
- 🎯 **Límites y Presupuestos:** Establece topes de gasto por categoría (incluyendo categorías personalizadas). El sistema te alertará si estás a punto de quedar en rojo.
- 📱 **Diseño Responsivo y Accesible:** Interfaz gráfica moderna (CustomTkinter) optimizada tanto para monitores Full HD como para pantallas estándar (1024x720). Incluye sistema de zoom visual (80% a 150%).
- 💾 **Exportación y Respaldo:** Exporta tus reportes financieros a CSV, Excel (.xlsx) o TXT. Incluye sistema nativo para crear y restaurar copias de seguridad (Backups JSON).

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3
- **Interfaz Gráfica:** CustomTkinter
- **Visualización de Datos:** Matplotlib, FigureCanvasTkAgg
- **Almacenamiento de Datos:** Manejo de archivos locales (`.txt`, `.json`)
- **Exportación:** OpenPyXL (Excel), CSV

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/TuUsuario/Gestor-de-Gastos-Personales.git
   cd Gestor-de-Gastos-Personales
   ```

2. **Instalar las dependencias necesarias:**
   Asegúrate de tener Python instalado y ejecuta:
   ```bash
   pip install customtkinter matplotlib openpyxl
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python App_Grafica_3.py
   ```

## 📂 Estructura de Datos
El proyecto está pensado para funcionar 100% offline, respetando la privacidad del usuario.
- `gastos.txt`: Almacena de forma ligera el presupuesto actual y el historial cronológico.
- `config.json`: Guarda preferencias de UI (tema, zoom), configuración de alertas, idiomas y diccionarios de categorías customizadas.
- `/comprobantes/`: Bóveda local autogenerada para almacenar respaldos de imágenes y PDFs.

## 👨‍💻 Desarrollador
Creado por **Mathias** - Estudiante de Ingeniería Informática, Universidad de Valparaíso.