import json
from typing import List, Dict, Any
from collections import defaultdict


def count_transactions(transactions: List[Dict[str, Any]],
                       categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    :param transactions: Список словарей с транзакциями
    :param categories: Список интересующих категорий
    :return: Словарь {категория: количество}
    """
    result = defaultdict(int)

    for operation in transactions:
        if 'description' in operation and operation['description'] in categories:
            result[operation['description']] += 1

    return dict(result)


def main():
    """Основная функция программы"""
    print("Анализатор банковских операций")
    print("=" * 30)

    try:
        # Загрузка данных из файла
        with open('operations.json', 'r', encoding='utf-8') as f:
            all_transactions = json.load(f)

        if not isinstance(all_transactions, list):
            print("Ошибка: файл должен содержать список операций")
            return

        # Пример использования
        interesting_categories = [
            'Перевод со счета на счет',
            'Открытие вклада'
        ]

        result = count_transactions(all_transactions, interesting_categories)

        print("\nРезультат подсчета операций:")
        for category, count in result.items():
            print(f"{category}: {count}")

        print("\nВсего операций:", len(all_transactions))

    except FileNotFoundError:
        print("Ошибка: файл operations.json не найден")
    except json.JSONDecodeError:
        print("Ошибка: файл содержит некорректные JSON-данные")
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")


if __name__ == "__main__":
    main()
