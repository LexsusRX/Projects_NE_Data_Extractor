import pandas as pd
import os
from config import EXCEL_COLUMNS # Используем EXCEL_COLUMNS
from logger_config import logger

class ExcelWriter:
    """Класс для записи данных в XLSX файл."""

    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def write_to_excel(self, data, filename): # Убран info_type
        """
        Записывает список словарей (данные) в XLSX файл.
        """
        if not data:
            logger.info("Нет данных для записи в Excel.")
            return

        df = pd.DataFrame(data, columns=EXCEL_COLUMNS) # Используем EXCEL_COLUMNS
        filepath = os.path.join(self.output_dir, filename)

        try:
            df.to_excel(filepath, index=False)
            logger.info(f"Данные успешно записаны в: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Ошибка при записи в Excel файл {filepath}: {e}")
            return None
            