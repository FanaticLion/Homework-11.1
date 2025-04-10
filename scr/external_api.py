import requests
def convert_currency_to_rub(transaction):
    """
    Конвертирует сумму транзакции в рубли, если валюта указана как USD или EUR.

    :param transaction: Словарь с данными о транзакции (например, {'amount': 100, 'currency': 'USD'}).
    :return: Сумма транзакции в рублях (тип float).
    """
    amount = transaction.get('amount', 0)
    currency = transaction.get('currency', '').upper()

    if currency not in ['USD', 'EUR']:
        # Если валюта уже в рублях или неизвестна, возвращаем сумму без изменений
        return float(amount)

    # Получение текущего курса соответствующей валюты
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
        if response.status_code == 200:
            rates = response.json().get('rates', {})
            rub_rate = rates.get('RUB', 1)  # Получаем курс RUB, если он есть
            return float(amount) * rub_rate
        else:
            print(f"Не удалось получить курс для {currency}. Статус: {response.status_code}")
            return 0.0
    except requests.RequestException as e:
        print(f"Ошибка при соединении с API: {e}")
        return 0.0