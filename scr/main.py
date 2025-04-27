from typing import List, Dict, Any
from scr.utils import filter_transactions, count_transactions  # Используемый импорт


def load_sample_data() -> List[Dict[str, Any]]:
    """Загружает тестовые данные транзакций"""
    return [
        {"description": "Покупка продуктов", "status": "completed"},
        {"description": "Оплата интернета", "status": "pending"},
        {"description": "Перевод другу", "status": "completed"},
    ]


def get_categories() -> Dict[str, List[str]]:
    """Возвращает категории для анализа"""
    return {
        "Продукты": ["покупка", "продукты"],
        "Коммунальные": ["оплата", "интернет"],
        "Переводы": ["перевод"]
    }


def main():
    """Основная функция программы"""
    transactions = load_sample_data()
    categories = get_categories()

    # Пример использования импортированных функций
    filtered = filter_transactions(transactions, "покупка")
    stats = count_transactions(transactions, categories)

    print("Отфильтрованные транзакции:", filtered)
    print("Статистика по категориям:", stats)


if __name__ == "__main__":
    main()