import os
from config import INPUT_DIR, OUTPUT_DIR, get_output_filename
from file_processor import FileProcessor
from data_parser import DataParser
from excel_writer import ExcelWriter
from logger_config import logger


# --- ВЕРСИЯ ПРИЛОЖЕНИЯ ---
__version__ = "1.0.2"

#1.0.2 версия для запаковки в EXE, исправлены мелкие баги, добавлего логирование

def main():
    """Основная функция для выполнения скрипта."""
    file_processor = FileProcessor(INPUT_DIR)
    excel_writer = ExcelWriter(OUTPUT_DIR)
    
    logger.info("Начинаем извлечение основной информации NE.")

    zip_archives = file_processor.get_zip_archives()

    if not zip_archives:
        logger.info(f"Не найдено ZIP-архивов в папке '{INPUT_DIR}'. Пожалуйста, положите архивы туда.")
        logger.info(f"Пример: создайте папку '{INPUT_DIR}' в корне проекта и положите в неё 'ваш_архив.zip'")
        return

    all_parsed_data = [] # Список для сбора данных со всех файлов и архивов

    for archive_path in zip_archives:
        logger.info(f"Обработка архива: {os.path.basename(archive_path)}")
        extracted_ne_data_files = file_processor.find_and_extract_ne_data(archive_path)
        
        if not extracted_ne_data_files:
            logger.warning(f"В архиве '{os.path.basename(archive_path)}' не найдено файлов, начинающихся на 'NEData' и с расширением '.txt'.")
            continue

        for filename, content in extracted_ne_data_files:
            logger.info(f"  Парсинг файла: {filename}")
            parser = DataParser(content) # Убран filename
            parsed_data = parser.parse()
            if parsed_data:
                all_parsed_data.append(parsed_data)
        
    if all_parsed_data:
        # Имя выходного файла будет формироваться от имени первого архива, но это можно изменить
        # Если вы хотите один общий файл для всех архивов, используем фиксированное имя или имя первого архива
        # Для простоты пока используем имя первого архива для формирования имени файла
        output_filename = get_output_filename(os.path.basename(zip_archives[0])) 
        excel_writer.write_to_excel(all_parsed_data, output_filename)
    else:
        logger.warning(f"Не удалось извлечь данные из файлов NEData.")

if __name__ == "__main__":
    main()
    