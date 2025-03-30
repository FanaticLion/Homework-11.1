def filter_by_currency(data_list, currency_code):
    """
    Фильтрует список транзакций по указанному коду валюты.

    Args:
        data_list (list): Список транзакций (список словарей).
        currency_code (str): Код валюты для фильтрации (например, "USD").

    Yields:
        dict: Транзакции, где код валюты совпадает с указанным.
    """
    if not isinstance(data_list, list):
        raise ValueError("data_list должен быть списком словарей.")

    for item in data_list:
        if not isinstance(item, dict):
            raise ValueError("Каждый элемент data_list должен быть словарем.")

        # Получаем информацию о валюте из ключа "operationAmount"
        operation_amount = item.get("operationAmount")
        if operation_amount and isinstance(operation_amount, dict):
            currency = operation_amount.get("currency")
            if currency and currency.get("code") == currency_code:
                yield item


def transaction_descriptions(data_list):
    """
    Генератор, возвращающий описания транзакций из списка словарей.

    Args:
        data_list (list): Список словарей, представляющих транзакции.

    Yields:
        str: Значение ключа 'description' для каждой транзакции, если оно существует.
    """
    if not isinstance(data_list, list):
        raise ValueError("data_list должен быть списком словарей.")

    for transaction in data_list:
        if not isinstance(transaction, dict):
            raise ValueError("Каждый элемент data_list должен быть словарем.")

        # Проверяем наличие ключа "description" и возвращаем его значение
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start, stop):
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start (int): Начальный номер диапазона (например, 1).
        stop (int): Конечный номер диапазона (например, 5).

    Yields:
        str: Сгенерированный номер карты в формате XXXX XXXX XXXX XXXX.
    """
    if not isinstance(start, int) or not isinstance(stop, int):
        raise ValueError("start и stop должны быть целыми числами.")
    if start <= 0 or stop > 10 ** 16:  # Номера карт не могут превышать 16 цифр
        raise ValueError("Диапазон должен быть от 1 до 9999999999999999.")
    if start > stop:
        raise ValueError("start должен быть меньше или равен stop.")

    for number in range(start, stop + 1):
        # Преобразуем число в строку длиной 16 символов с ведущими нулями
        card_number = f"{number:016d}"
        # Форматируем строку в виде XXXX XXXX XXXX XXXX
        formatted_card_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_card_number