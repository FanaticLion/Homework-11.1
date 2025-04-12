import requests
from typing import Dict, Union

API_KEY = "7pKg6vOlC07cqRKmLl9RlPEUXgoXC7Or"
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_currency_to_rub(transaction: Dict[str, Union[str, float]]) -> float:
    """
    Конвертирует сумму транзакции в рубли, используя текущий курс валют.

    :param transaction: Словарь с данными о транзакции (например, {'amount': 100, 'currency': 'USD'}).
    :return: Сумма транзакции в рублях (float). Если валюта не USD/EUR или API недоступно, возвращает исходную сумму.
    """
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", "").upper()

    # Если валюта уже в рублях или неизвестна, возвращаем сумму без изменений
    if currency not in ["USD", "EUR"]:
        return amount

    # Запрос к API для получения курса
    try:
        response = requests.get(
            BASE_URL,
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=5
        )
        response.raise_for_status()  # Проверка на ошибки HTTP

        data = response.json()
        rub_rate = data.get("rates", {}).get("RUB", 1.0)
        return amount * rub_rate

    except (requests.RequestException, KeyError) as e:
        print(f"Ошибка при конвертации валюты: {e}")
        return amount  # Возвращаем исходную сумму при ошибке