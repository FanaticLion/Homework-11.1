import pytest
from scr.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Фикстура: Пример транзакций
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Оплата счета",
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод на карту",
        },
        {
            "id": 4,  # Транзакция без ключа "operationAmount"
            "description": "Проверка данных",
        },
        {
            "id": 5,  # Транзакция без ключа "description"
            "operationAmount": {"currency": {"code": "EUR"}},
        },
    ]


# Фикстура: Пример диапазона для генерации номеров карт
@pytest.fixture
def card_range():
    return 1, 5


# Тесты для filter_by_currency

def test_filter_by_currency_valid(sample_transactions):
    # Проверка: валидный фильтр для USD
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert result == [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод на карту"},
    ]


def test_filter_by_currency_no_match(sample_transactions):
    # Проверка: отсутствие совпадений
    result = list(filter_by_currency(sample_transactions, "GBP"))
    assert result == []


def test_filter_by_currency_empty_list():
    # Проверка: пустой список транзакций
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_missing_operation_amount(sample_transactions):
    # Проверка: транзакции без ключа "operationAmount" игнорируются
    result = list(filter_by_currency(sample_transactions, "RUB"))
    assert result == [{"id": 2, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Оплата счета"}]


def test_filter_by_currency_invalid_data():
    # Проверка: некорректный тип данных
    with pytest.raises(ValueError, match="data_list должен быть списком словарей."):
        list(filter_by_currency("not a list", "USD"))

    with pytest.raises(ValueError, match="Каждый элемент data_list должен быть словарем."):
        list(filter_by_currency([{}, "not dict"], "USD"))


# Тесты для transaction_descriptions

def test_transaction_descriptions_valid(sample_transactions):
    # Проверка: все описания транзакций
    result = list(transaction_descriptions(sample_transactions))
    assert result == ["Перевод организации", "Оплата счета", "Перевод на карту", "Проверка данных"]


def test_transaction_descriptions_missing_description(sample_transactions):
    # Проверка: транзакции без "description" игнорируются
    transactions_without_description = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 2},  # Без ключа "description"
    ]
    result = list(transaction_descriptions(transactions_without_description))
    assert result == ["Перевод организации"]


def test_transaction_descriptions_empty_list():
    # Проверка: пустой список транзакций
    result = list(transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_invalid_data():
    # Проверка: некорректные данные
    with pytest.raises(ValueError, match="data_list должен быть списком словарей."):
        list(transaction_descriptions("not a list"))

    with pytest.raises(ValueError, match="Каждый элемент data_list должен быть словарем."):
        list(transaction_descriptions([{}, "not dict"]))


# Тесты для card_number_generator

def test_card_number_generator_valid(card_range):
    # Проверка: генерация номеров карт в заданном диапазоне
    start, stop = card_range
    result = list(card_number_generator(start, stop))
    assert result == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


def test_card_number_generator_one_number():
    # Проверка: генерация одного номера карты
    result = list(card_number_generator(1, 1))
    assert result == ["0000 0000 0000 0001"]


def test_card_number_generator_large_range():
    # Проверка: генерация большого диапазона номеров карт
    result = list(card_number_generator(9999999999999995, 9999999999999999))
    assert result == [
        "9999 9999 9999 9995",
        "9999 9999 9999 9996",
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999",
    ]


def test_card_number_generator_invalid_range():
    # Проверка: некорректный диапазон (start > stop)
    with pytest.raises(ValueError, match="start должен быть меньше или равен stop."):
        list(card_number_generator(10, 1))


def test_card_number_generator_out_of_bounds():
    # Проверка: выход за допустимый диапазон
    with pytest.raises(ValueError, match="Диапазон должен быть от 1 до 9999999999999999."):
        list(card_number_generator(0, 10 ** 16 + 1))
