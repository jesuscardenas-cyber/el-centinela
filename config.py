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

# Token predeterminado para API de facebook Graph (TIEMPO LIMITADO DE USO 1HR SE UTILIZARA ACCES TOKEN DEBBUGER PARA AMPLIAR A 60 DÍAS)
FBB_ACCES_TOKEN = "EAAMmT2HyA58BST7NZBZCfoDuhRaLLkMGzYQDjBs2Q2YLUGmXJERwbnue5RMc8jAQeaDkWq16nroi9OeNSAhGYC4T5binhLQuDAChVGLZC4cNxdGOLrwVP8zyk2XMH6k4UdZCDohzWljkxmCmZC20cPoQqX0RCyaTqtnZAq3bcZBCD22rNNXSMKUXoZBraQwcZAyLbMJMFBaHj6GmEvMksKEJ9yMAVNv0uHuLXZBwTKFa0pJBL8QMHbF5pUIkdTCUKy9HF12haUfMIBObhs2Uul6mciZCPjeqQZDZD"
