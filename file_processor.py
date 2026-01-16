import zipfile
import os
from config import NE_DATA_FILE_PREFIX
from logger_config import logger

class FileProcessor:
    """Класс для обработки ZIP-архивов и извлечения нужных файлов."""

    def __init__(self, input_dir):
        self.input_dir = input_dir

    def find_and_extract_ne_data(self, zip_filepath):
        """
        Находит и извлекает файлы NEData_*.txt из ZIP-архива.
        Возвращает список кортежей (имя файла, содержимое файла).
        """
        extracted_data = []
        try:
            with zipfile.ZipFile(zip_filepath, 'r') as zf:
                for member in zf.namelist():
                    if member.startswith(NE_DATA_FILE_PREFIX) and member.lower().endswith(".txt"):
                        try:
                            for encoding in ['utf-8', 'cp1251', 'latin-1']:
                                try:
                                    with zf.open(member) as f:
                                        content = f.read().decode(encoding)
                                    extracted_data.append((os.path.basename(member), content))
                                    break
                                except UnicodeDecodeError:
                                    continue
                            else:
                                logger.warning(f"Не удалось декодировать файл {member} из архива {zip_filepath} ни одной из известных кодировок.")

                        except Exception as e:
                            logger.error(f"Ошибка при чтении файла {member} из архива {zip_filepath}: {e}")
        except FileNotFoundError:
            logger.error(f"Архив не найден: {zip_filepath}")
        except zipfile.BadZipFile:
            logger.error(f"Некорректный ZIP-файл: {zip_filepath}")
        except Exception as e:
            logger.error(f"Общая ошибка при обработке архива {zip_filepath}: {e}")
        return extracted_data

    def get_zip_archives(self):
        """Возвращает список полных путей до ZIP-архивов в папке Input."""
        zip_files = []
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)
            logger.info(f"Создана директория Input: {self.input_dir}")
            return []

        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith(".zip"):
                zip_files.append(os.path.join(self.input_dir, filename))
        return zip_files
        