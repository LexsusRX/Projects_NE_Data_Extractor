import os
from config import INPUT_DIR, OUTPUT_DIR, get_output_filename
from file_processor import FileProcessor
from data_parser import DataParser
from excel_writer import ExcelWriter


# --- ВЕРСИЯ ПРИЛОЖЕНИЯ ---
__version__ = "1.0.1"

def main():
    """Основная функция для выполнения скрипта."""
    file_processor = FileProcessor(INPUT_DIR)
    excel_writer = ExcelWriter(OUTPUT_DIR)
    
    # Получаем список всех ZIP-архивов в папке Input
    zip_archives = file_processor.get_zip_archives()

    if not zip_archives:
        print(f"Не найдено ZIP-архивов в папке '{INPUT_DIR}'. Пожалуйста, положите архивы туда.")
        print(f"Пример: создайте папку '{INPUT_DIR}' в корне проекта и положите в неё 'ваш_архив.zip'")
        return

    for archive_path in zip_archives:
        print(f"\nОбработка архива: {os.path.basename(archive_path)}")
        extracted_ne_data_files = file_processor.find_and_extract_ne_data(archive_path)
        
        if not extracted_ne_data_files:
            print(f"В архиве '{os.path.basename(archive_path)}' не найдено файлов, начинающихся на 'NEData' и с расширением '.txt'.")
            continue

        all_parsed_data_for_archive = []
        for filename, content in extracted_ne_data_files:
            print(f"  Парсинг файла: {filename}")
            parser = DataParser(content)
            parsed_data = parser.parse()
            if parsed_data:
                all_parsed_data_for_archive.append(parsed_data)
        
        if all_parsed_data_for_archive:
            output_filename = get_output_filename(os.path.basename(archive_path))
            excel_writer.write_to_excel(all_parsed_data_for_archive, output_filename)
        else:
            print(f"Не удалось извлечь данные из файлов NEData в архиве '{os.path.basename(archive_path)}'.")

if __name__ == "__main__":
    main()
    