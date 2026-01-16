import re

class DataParser:
    """Класс для парсинга данных из содержимого NEData файла."""

    def __init__(self, file_content):
        self.file_content = file_content
        self.parsed_data = {}

    def parse(self):
        """Парсит весь файл и извлекает необходимые данные."""
        self._parse_cfg_nepara()
        self._parse_ne_board_info()
        return self.parsed_data

    def _parse_cfg_nepara(self):
        """Извлекает данные из блока :cfg-nepara:."""
        match = re.search(r':cfg-nepara:\{(.*?)\};', self.file_content, re.DOTALL)
        if match:
            params_str = match.group(1)
            params = self._parse_key_value_pairs(params_str)
            self.parsed_data["NE name"] = params.get("name", "").strip('"')
            self.parsed_data["NE ID"] = params.get("neid", "").strip('"')
            self.parsed_data["Creator"] = params.get("creater", "").strip('"')
            self.parsed_data["Buildtime"] = params.get("buildtime", "").strip('"')
            self.parsed_data["Device"] = params.get("device", "").strip('"')

    def _parse_ne_board_info(self):
        """Извлекает серийные номера из блока NeBoardInfo."""
        serial_numbers = []
        # Ищем блок NeBoardInfo
        board_info_block_match = re.search(r'\[NeBoardInfo\].*?(\s*\{.*?\}\s*\[Board Properties\].*?BarCode=.*?\])+', self.file_content, re.DOTALL)
        if board_info_block_match:
            board_info_block = board_info_block_match.group(0)
            # Ищем все BarCode в блоках [Board Properties]
            barcodes = re.findall(r'\[Board Properties\].*?BarCode=(.*?)\n', board_info_block, re.DOTALL)
            for barcode in barcodes:
                barcode = barcode.strip().replace('"', '')
                if barcode: # Проверяем только, что строка не пустая
                    serial_numbers.append(barcode)
        
        self.parsed_data["Serial Number"] = ", ".join(serial_numbers) if serial_numbers else ""


    def _parse_key_value_pairs(self, text):
        """Парсит пары ключ=значение из строки параметров."""
        pairs = {}
        pattern = r'(\w+)\s*=\s*(?:(".*?"|\[.*?\]|\{.*?\}|[^\s,]+))(?:\s*,\s*|$)'
        
        parts = []
        in_quotes = False
        start = 0
        for i, char in enumerate(text):
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(text[start:i])
                start = i + 1
        parts.append(text[start:])

        for part in parts:
            part = part.strip()
            if not part:
                continue

            match = re.match(r'(\w+)\s*=\s*(.*)', part)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                pairs[key] = value
        return pairs
        