import json
from typing import List, Dict, Any
import os
import logging

#Настройка логгера для модуля utils
utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# Создаем file handler
file_handler = logging.FileHandler('utils.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем formatter
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
utils_logger.addHandler(file_handler)

def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о транзакциях из JSON-файла.

    :param file_path: Путь до JSON-файла с транзакциями.
    :return: Список словарей с данными о транзакциях.
    """
    try:
        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            utils_logger.warning(f"Файл не найден: {file_path}")
            return []

        # Открываем файл и загружаем JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            utils_logger.debug(f"Успешно загружен файл: {file_path}")

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            utils_logger.debug(f"Успешно загружено {len(data)} транзакций")
            return data
        else:
            utils_logger.warning("Файл не содержит список транзакций")
            return []

    except json.JSONDecodeError as e:
        utils_logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except FileNotFoundError:
        utils_logger.error(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        utils_logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {str(e)}")
        return []

# Пример использования:
if __name__ == "__main__":
    transactions = load_transactions("../data/operations.json")
    print(transactions)



