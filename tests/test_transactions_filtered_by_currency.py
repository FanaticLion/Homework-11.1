import pytest
from scr.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Фикстуры
@pytest.fixture
def transactions_data():
    return [
        {"currency": "USD", "amount": 100, "description": "Payment at Store A"},
        {"currency": "EUR", "amount": 200, "description": "Purchase at Store B"},
        {"currency": "USD", "amount": 150, "description": "Refund from Store C"},
        {"currency": "JPY", "amount": 1000, "description": "Purchase in Japan"},
    ]


# Тесты для filter_by_currency
@pytest.mark.parametrize(
    "currency, expected",
    [
        ("USD", [
            {"currency": "USD", "amount": 100, "description": "Payment at Store A"},
            {"currency": "USD", "amount": 150, "description": "Refund from Store C"},
        ]),
        ("EUR", [
            {"currency": "EUR", "amount": 200, "description": "Purchase at Store B"},
        ]),
        ("JPY", [
            {"currency": "JPY", "amount": 1000, "description": "Purchase in Japan"},
        ]),
        ("GBP", []),
    ],
)
def test_filter_by_currency(transactions_data, currency, expected):
    result = list(filter_by_currency(transactions_data, currency))
    assert result == expected, f"Expected {expected}, but got {result}"


@pytest.mark.parametrize(
    "data_list, currency, exception_message",
    [
        ("invalid_data", "USD", "data_list must be a list of dictionaries."),
        ([{"currency": "USD"}, "invalid_element"], "USD", "All elements in data_list must be dictionaries."),
    ],
)
def test_filter_by_currency_invalid_input(data_list, currency, exception_message):
    with pytest.raises(ValueError, match=exception_message):
        list(filter_by_currency(data_list, currency))


# Тесты для transaction_descriptions
@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                {"currency": "USD", "amount": 100, "description": "Payment at Store A"},
                {"currency": "EUR", "amount": 200, "description": "Purchase at Store B"},
                {"currency": "USD", "amount": 150, "description": "Refund from Store C"},
                {"currency": "JPY", "amount": 1000, "description": "Purchase in Japan"},
            ],
            ["Payment at Store A", "Purchase at Store B", "Refund from Store C", "Purchase in Japan"],
        ),
        ([], []),  # Пустой список транзакций
    ],
)
def test_transaction_descriptions(transactions, expected):
    result = list(transaction_descriptions(transactions))
    assert result == expected, f"Expected {expected}, but got {result}"


@pytest.mark.parametrize(
    "data_list, exception_message",
    [
        ("invalid_data", "data_list должен быть списком словарей."),
        ([{"description": "Payment"}, "invalid_item"], "Каждый элемент data_list должен быть словарем."),
    ],
)
def test_transaction_descriptions_invalid_input(data_list, exception_message):
    with pytest.raises(ValueError, match=exception_message):
        list(transaction_descriptions(data_list))


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 5, ["CARD-00000001", "CARD-00000002", "CARD-00000003", "CARD-00000004"]),
        (10, 12, ["CARD-00000010", "CARD-00000011"]),
    ],
)
def test_card_number_generator_range(start, stop, expected):
    result = list(card_number_generator(start, stop))
    assert result == expected, f"Expected {expected}, but got {result}"


@pytest.mark.parametrize(
    "start, stop, exception_message",
    [
        ("a", 10, "start и stop должны быть целыми числами."),
        (10, 10, "start должен быть меньше stop."),
        (20, 10, "start должен быть меньше stop."),
    ],
)
def test_card_number_generator_invalid_input(start, stop, exception_message):
    with pytest.raises(ValueError, match=exception_message):
        list(card_number_generator(start, stop))
