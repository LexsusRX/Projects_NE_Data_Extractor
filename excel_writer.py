import pandas as pd
import os
from config import OUTPUT_DIR, EXCEL_COLUMNS

class ExcelWriter:
    """Класс для записи данных в XLSX файл."""

    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def write_to_excel(self, data, filename):
        """
        Записывает список словарей (данные) в XLSX файл.
        :param data: Список словарей, где каждый словарь - строка данных.
        :param filename: Имя файла для сохранения.
        """
        if not data:
            print("Нет данных для записи в Excel.")
            return

        df = pd.DataFrame(data, columns=EXCEL_COLUMNS)
        filepath = os.path.join(self.output_dir, filename)

        try:
            df.to_excel(filepath, index=False)
            print(f"Данные успешно записаны в: {filepath}")
            return filepath
        except Exception as e:
            print(f"Ошибка при записи в Excel файл {filepath}: {e}")
            return None

            