def filter_by_currency(data_list, currency):
    """
    Фильтрует список транзакций по указанной валюте.
    """
    if not isinstance(data_list, list):
        raise ValueError("data_list must be a list of dictionaries.")

    for item in data_list:
        if not isinstance(item, dict):
            raise ValueError("All elements in data_list must be dictionaries.")
        if item.get("currency") == currency:
            yield item


def transaction_descriptions(data_list):
    """
    Генератор, возвращающий описания транзакций из списка словарей.

    Args:
        data_list (list): Список словарей, представляющих транзакции.

    Yields:
        str: Значение ключа 'description' для каждой транзакции.
    """
    if not isinstance(data_list, list):
        raise ValueError("data_list должен быть списком словарей.")

    for transaction in data_list:
        if not isinstance(transaction, dict):
            raise ValueError("Каждый элемент data_list должен быть словарем.")

        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start, stop):
    """
    Генерирует номера карт в заданном диапазоне.
    Каждая карта должна начинаться с 'CARD-' и содержать ровно 8 цифр после префикса.
    Например: CARD-00000001.
    """
    if not isinstance(start, int) or not isinstance(stop, int):
        raise ValueError("start и stop должны быть целыми числами.")
    if start >= stop:
        raise ValueError("start должен быть меньше stop.")

    for num in range(start, stop):
        # Формат номера карты с 8-значным числом.
        yield f"CARD-{num:08d}"
