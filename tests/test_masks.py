import pytest
from scr.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number() -> None:
    """Функция тестирования масок карт"""

    # Тесты на корректное поведение функции
    assert get_mask_card_number("21541221421212525845") == "2154 12 ** **** **** 5845"
    assert get_mask_card_number("12341234123412345678") == "1234 12 ** **** **** 5678"

    # Тестирование исключений
    with pytest.raises(ValueError, match="Card number is too short"):

        get_mask_card_number("215412214212125")  # Слишком короткий номер
    with pytest.raises(ValueError, match="Card number is empty"):
        get_mask_card_number("")  # Пустая строка


def test_get_mask_account() -> None:
    """Функция тестирования масок счетов"""

    # Корректное поведение с различной длиной строк
    assert get_mask_account("1234567890") == "****7890", "Ожидаемая маска '****7890'"
    assert get_mask_account("12345678901234567890") == "****567890", "Ожидаемая маска '****567890'"
    # Пограничный случай с минимальным допустимым количеством символов (4)
    assert get_mask_account("1234") == "****1234", "Ожидаемая маска '****1234'"

    # Тест на выброс исключений
    with pytest.raises(ValueError, match="Содержит недопустимые символы."):
        get_mask_account("12a45")  # Содержит недопустимые символы

    with pytest.raises(ValueError, match="Номер счёта должен содержать минимум 4 цифры."):
        get_mask_account(" ")  # Пустое значение

    with pytest.raises(ValueError, match="Номер счёта должен содержать минимум 4 цифры."):
        get_mask_account("123")  # Слишком короткий номер

    with pytest.raises(ValueError, match="Номер счёта должен содержать минимум 4 цифры."):
        get_mask_account("")  # Пустая строка
