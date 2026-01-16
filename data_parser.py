import re
from logger_config import logger

class DataParser:
    """Класс для парсинга данных из содержимого NEData файла."""

    def __init__(self, file_content): # Убран filename, т.к. не нужен для NE Name (File)
        self.file_content = file_content
        self.parsed_data = {}

    def parse(self):
        """Парсит основную информацию NE из блока :cfg-nepara:."""
        match = re.search(r':cfg-nepara:\{(.*?)\};', self.file_content, re.DOTALL)
        if match:
            params_str = match.group(1)
            params = self._parse_key_value_pairs(params_str)
            
            self.parsed_data["NE Name"] = params.get("name", "").strip('"')
            self.parsed_data["NE ID"] = params.get("neid", "").strip('"')
            self.parsed_data["Creator"] = params.get("creater", "").strip('"')
            self.parsed_data["Buildtime"] = params.get("buildtime", "").strip('"')
            self.parsed_data["Device"] = params.get("device", "").strip('"')
            self.parsed_data["vrc_ver"] = params.get("vrc_ver", "").strip('"')
            self.parsed_data["ip"] = params.get("ip", "").strip('"')
        else:
            logger.warning("Блок ':cfg-nepara:' не найден в файле.")
            
        return self.parsed_data

    def _parse_key_value_pairs(self, text):
        """
        Парсит пары ключ=значение из строки параметров.
        """
        pairs = {}
        # Регулярное выражение для более надежного парсинга
        # Захватываем ключ (\w+)
        # Затем знак равенства =
        # Затем значение, которое может быть:
        # 1. Строка в двойных кавычках ("...")
        # 2. Или любой текст, не содержащий запятую или новую строку, до следующего параметра или конца блока
        # Используем (?:...) для не-захватывающей группы для разделителя
        pattern = r'(\w+)\s*=\s*(?:(".*?")|([^,\n]+?))(?:\s*,\s*|(?=\n)|$)'
        
        for match in re.finditer(pattern, text, re.DOTALL):
            key = match.group(1).strip()
            # match.group(2) - для строк в кавычках, match.group(3) - для значений без кавычек
            # Берем первое непустое значение из этих двух групп
            value = match.group(2) if match.group(2) is not None else match.group(3)
            
            value = value.strip('"').strip() # Удаляем кавычки и лишние пробелы

            if not value:
                value = ""
            
            pairs[key] = value
        return pairs
        