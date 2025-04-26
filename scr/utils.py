import json
from typing import List, Dict, Any
import os
import logging
from pathlib import Path
import re
from collections import Counter

# Настройка логгера и директории для логов
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)
utils_logger.handlers.clear()

file_handler = logging.FileHandler(
    filename=logs_dir / "utils.log",
    mode='w',
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
utils_logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о транзакциях из JSON-файла.

    :param file_path: Путь до JSON-файла с транзакциями.
    :return: Список словарей с данными о транзакциях.
    """
    try:
        utils_logger.debug(f"Попытка загрузить файл: {file_path}")

        if not os.path.exists(file_path):
            utils_logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            utils_logger.debug(f"Успешно загружен файл: {file_path}")

        if isinstance(data, list):
            utils_logger.info(f"Успешно загружено {len(data)} транзакций")
            return data
        else:
            utils_logger.warning("Файл не содержит список транзакций")
            return []

    except json.JSONDecodeError as e:
        utils_logger.error(f"Ошибка декодирования JSON: {str(e)}")
        return []
    except Exception as e:
        utils_logger.error(f"Неожиданная ошибка: {str(e)}")
        return []


def search_transactions(
        transactions_list: List[Dict[str, Any]],
        search_string: str,
        case_sensitive: bool = False
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании.

    :param transactions_list: Список транзакций
    :param search_string: Строка для поиска
    :param case_sensitive: Учитывать регистр
    :return: Список найденных транзакций
    """
    try:
        utils_logger.debug(f"Поиск: '{search_string}' (case_sensitive={case_sensitive})")

        if not transactions_list:
            utils_logger.warning("Пустой список транзакций")
            return []

        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(search_string), flags)

        result = [t for t in transactions_list
                  if pattern.search(t.get('description', ''))]

        utils_logger.info(f"Найдено {len(result)} совпадений")
        return result

    except Exception as e:
        utils_logger.error(f"Ошибка поиска: {str(e)}")
        return []


def count_transactions_by_type(
        transactions: List[Dict[str, Any]],
        categories: Dict[str, List[str]],
        exact_match: bool = False
) -> Dict[str, int]:
    """
    Подсчитывает транзакции по категориям.

    :param transactions: Список транзакций
    :param categories: {категория: [ключевые_слова]}
    :param exact_match: Точное совпадение описания
    :return: {категория: количество}
    """
    try:
        utils_logger.debug(f"Подсчёт по {len(categories)} категориям")

        if not transactions:
            utils_logger.warning("Нет транзакций для анализа")
            return {}

        # Создаем словарь для поиска категории по ключевому слову
        keyword_to_category = {}
        for category, keywords in categories.items():
            for kw in keywords:
                keyword_to_category[kw.lower()] = category

        categorized = []
        for t in transactions:
            desc = t.get('description', '').lower()
            for kw, category in keyword_to_category.items():
                if (exact_match and kw == desc) or (not exact_match and kw in desc):
                    categorized.append(category)
                    break

        counts = dict(Counter(categorized))
        utils_logger.info(f"Результат подсчёта: {counts}")
        return counts

    except Exception as e:
        utils_logger.error(f"Ошибка подсчёта: {str(e)}")
        return {}


if __name__ == "__main__":
    # Пример использования
    test_transactions = [
        {'description': 'Покупка в Ашане', 'amount': 1500},
        {'description': 'Оплата интернета', 'amount': 500},
        {'description': 'Покупка продуктов', 'amount': 1200}
    ]

    test_categories = {
        'Продукты': ['ашан', 'покупка продуктов'],
        'Коммунальные': ['оплата интернета']
    }

    # Тестируем функции
    print("Все транзакции:", test_transactions)
    print("Поиск 'покупка':", search_transactions(test_transactions, "покупка"))
    print("Статистика по категориям:",
          count_transactions_by_type(test_transactions, test_categories))
