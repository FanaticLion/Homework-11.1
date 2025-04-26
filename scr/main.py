import re
from collections import Counter


def search_transactions(transactions, search_string):
    """Поиск транзакций по строке в описании"""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get('description', ''))]


def count_transactions_by_type(transactions, categories):
    """Подсчет операций по категориям"""
    description_to_category = {}
    for category, descriptions in categories.items():
        for desc in descriptions:
            description_to_category[desc.lower()] = category

    transaction_categories = []
    for transaction in transactions:
        description = transaction.get('description', '').lower()
        for desc_pattern, category in description_to_category.items():
            if desc_pattern in description:
                transaction_categories.append(category)
                break

    return dict(Counter(transaction_categories))


def display_transactions(transactions):
    """Отображение списка транзакций"""
    for idx, t in enumerate(transactions, 1):
        print(f"{idx}. {t['description']}: {t['amount']} руб.")


def main():
    """Основная функция проекта"""
    # Пример данных
    transactions = [
        {'description': 'Покупка в Ашане', 'amount': 1500},
        {'description': 'Оплата интернета', 'amount': 500},
        {'description': 'Зарплата', 'amount': 30000},
        {'description': 'Покупка продуктов', 'amount': 1200},
        {'description': 'Кафе Шоколадница', 'amount': 800},
    ]

    categories = {
        'Продукты': ['ашан', 'покупка продуктов', 'пятерочка'],
        'Коммунальные': ['оплата интернета', 'электричество'],
        'Доходы': ['зарплата'],
        'Кафе': ['кафе', 'шоколадница', 'ресторан']
    }

    while True:
        print("\n=== Личный финансовый менеджер ===")
        print("1. Поиск транзакций по описанию")
        print("2. Статистика по категориям")
        print("3. Показать все транзакции")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            search_term = input("Введите текст для поиска: ")
            found = search_transactions(transactions, search_term)
            print(f"\nНайдено {len(found)} транзакций:")
            display_transactions(found)

        elif choice == '2':
            stats = count_transactions_by_type(transactions, categories)
            print("\nСтатистика по категориям:")
            for category, count in stats.items():
                print(f"{category}: {count} операций")
            print(f"Всего категорий: {len(stats)}")

        elif choice == '3':
            print("\nВсе транзакции:")
            display_transactions(transactions)

        elif choice == '4':
            print("До свидания!")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите 1-4")


if __name__ == "__main__":
    main()
