import json
import os


def read_json_file(file_path):
    """
    Читает JSON-файл и возвращает список транзакций.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с данными о транзакциях или пустой список.
    """
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("JSON файл не содержит список.")
                return []
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON файла.")
        return []





