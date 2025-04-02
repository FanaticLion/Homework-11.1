
import pytest
from scr.processing import get_mask_card_number, filter_by_state, sort_by_date


def test_get_mask_card_number() -> None:
    """Тестирование функции get_mask_card_number"""

    # Тесты на корректное поведение
    assert get_mask_card_number("1234567812345678") == "**** **** ****5678"
    assert get_mask_card_number("0000111122223333") == "**** **** ****3333"

    # Тестирование исключений
    with pytest.raises(ValueError, match="Card number must contain only digits."):
        get_mask_card_number("1234abcd5678efgh")  # Номер карты содержит нецифровые символы

    with pytest.raises(ValueError, match="Номер карты должен содержать ровно 16 цифр."):
        get_mask_card_number("12345678")  # Номер карты слишком короткий

    with pytest.raises(ValueError, match="Номер карты должен содержать ровно 16 цифр."):
        get_mask_card_number("123456781234567890")  # Номер карты слишком длинный


def test_filter_by_state() -> None:
    """Тестирование функции filter_by_state"""

    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"}
    ]

    # Фильтрация по состоянию "EXECUTED"
    filtered = filter_by_state(transactions, state="EXECUTED")
    assert len(filtered) == 2
    assert filtered == [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]

    # Фильтрация по состоянию "CANCELED"
    filtered = filter_by_state(transactions, state="CANCELED")
    assert len(filtered) == 1
    assert filtered == [{"id": 2, "state": "CANCELED"}]

    # Фильтрация по состоянию, которого нет
    filtered = filter_by_state(transactions, state="APPROVED")
    assert len(filtered) == 0  # Ничего не найдено


def test_sort_by_date() -> None:
    """Тестирование функции sort_by_date"""

    transactions = [
        {"id": 1, "date": "2021-01-01T10:00:00.000000"},
        {"id": 2, "date": "2020-05-15T14:30:00.000000"},
        {"id": 3, "date": "2022-07-20T08:15:00.000000"}
    ]

    # Сортировка по убыванию
    sorted_transactions = sort_by_date(transactions, reverse=True)
    assert sorted_transactions == [
        {"id": 3, "date": "2022-07-20T08:15:00.000000"},
        {"id": 1, "date": "2021-01-01T10:00:00.000000"},
        {"id": 2, "date": "2020-05-15T14:30:00.000000"}
    ]

    # Сортировка по возрастанию
    sorted_transactions = sort_by_date(transactions, reverse=False)
    assert sorted_transactions == [
        {"id": 2, "date": "2020-05-15T14:30:00.000000"},
        {"id": 1, "date": "2021-01-01T10:00:00.000000"},
        {"id": 3, "date": "2022-07-20T08:15:00.000000"}
    ]

    # Ничего не передано в функцию (пустой список)
    sorted_transactions = sort_by_date([], reverse=True)
    assert sorted_transactions == []  # Результат тоже пустой список
