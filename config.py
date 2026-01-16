import os
from datetime import datetime

# Директории
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"

# Префикс для файлов NEData
NE_DATA_FILE_PREFIX = "NEData"

# --- Конфигурация для основной информации NE ---
EXCEL_COLUMNS = [
    "NE Name",
    "NE ID",
    "Creator",
    "Buildtime",
    "Device",
    "vrc_ver",
    "ip"
]

def get_output_filename(archive_name):
    """Генерирует имя выходного XLSX файла."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(archive_name)[0]
    return f"{base_name}_{timestamp}.xlsx"
    