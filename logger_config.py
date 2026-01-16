import logging
import os


# Директория для логов
LOG_DIR = "logs"
LOG_FILE_NAME = "script_log.log"

def setup_logging():
    """Настраивает систему логирования для вывода в файл и консоль."""
    
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_filepath = os.path.join(LOG_DIR, LOG_FILE_NAME)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG) # Общий минимальный уровень для всех обработчиков

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Консольный обработчик (вывод в терминал)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # В консоль выводим только INFO и выше
    console_handler.setFormatter(formatter)
    
    # Файловый обработчик (вывод в файл)
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(logging.INFO) # В файл пишем только INFO и выше (убрали DEBUG)
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()
