# =============================================================================
# config.py – Globální konfigurace aplikace Python Toolbox
# =============================================================================

# --- Aplikace ---
APP_NAME = "Python Toolbox"
APP_VERSION = "1.0.0"
APP_ICON = "🚛🚂⚓"

# --- Design (firemní barvy) ---
PRIMARY_COLOR = "#1E3A5F"
ACCENT_COLOR = "#4A90D9"
BACKGROUND_COLOR = "#F5F7FA"

# --- Soubory ---
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".csv"]

# --- Nominatim API (geokódování PSČ → lon/lat) ---
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_USER_AGENT = "python_toolbox_app/1.0"
NOMINATIM_DELAY_S = 1.0
NOMINATIM_TIMEOUT_S = 10

# --- OSRM API (výpočet vzdálenosti) ---
OSRM_URL_TEMPLATE = "http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
OSRM_TIMEOUT_S = 10

# --- CSV sloupce (PSČ kalkulačka) ---
CSV_COL_FROM_ZIP     = "z_PSČ"
CSV_COL_FROM_COUNTRY = "z_Země"
CSV_COL_TO_ZIP       = "do_PSČ"
CSV_COL_TO_COUNTRY   = "do_Země"
CSV_REQUIRED_COLUMNS = [CSV_COL_FROM_ZIP, CSV_COL_FROM_COUNTRY, CSV_COL_TO_ZIP, CSV_COL_TO_COUNTRY]

# --- Výstupní sloupce ---
CSV_COL_DISTANCE_KM = "vzdalenost_km"
CSV_COL_STATUS      = "stav"
CSV_STATUS_OK       = "ok"
CSV_STATUS_ERROR    = "chyba"

# --- XLSX procesor – pořadí sloupců ---
XLSX_COLUMN_SEQUENCE = [
    "Popisky řádků",
    "LOVODASA 26+13S",
    "LOVOFERT LAD 27",
    "LOVOFERT LAS 24+6S",
    "LOVOFERT LAV 27",
    "LOVOFERT CN 15",
    "LOVOFERT CN 15,5 GG",
    "LOVOFERT CN 15,5 GG+B",
    "LOVODAM 30",
    "ZENFERT 24 N",
    "LOVOFERT CN 15+B",
    "Celkový součet",
]