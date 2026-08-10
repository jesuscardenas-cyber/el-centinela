from pathlib import Path

# Carpeta raíz
ROOT_DIR = Path(__file__).parent

# Directorios
SALIDAS_DIR = ROOT_DIR / "salidas"
CSV_DIR = SALIDAS_DIR / "csv"
EXCEL_DIR = SALIDAS_DIR / "excel"
LOG_DIR = ROOT_DIR / "logs"

# Configuración Google News
GOOGLE_NEWS_LANGUAGE = "es-419"
GOOGLE_NEWS_COUNTRY = "MX"

# Configuración de búsqueda
MAX_RESULTADOS = 100

# Número máximo de consultas procesadas por lote
BATCH_SIZE = 10

# Máximo de hilos concurrentes
MAX_WORKERS = 8

# Número máximo de reintentos para tareas fallidas
MAX_RETRIES = 2
