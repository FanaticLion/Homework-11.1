import json
from typing import List, Dict, Any
import os


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о транзакциях из JSON-файла.

    :param file_path: Путь до JSON-файла с транзакциями.
    :return: Список словарей с данными о транзакциях. Если файл не найден, пуст или содержит не список, возвращает [].
    """
    try:
        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            return []

        # Открываем файл и загружаем JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, FileNotFoundError):
        # Если файл пуст, битый или не JSON
        return []


# Пример использования:
if __name__ == "__main__":
    transactions = load_transactions("../data/operations.json")
    print(transactions)




