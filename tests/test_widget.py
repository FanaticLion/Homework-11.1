import pytest
from scr.widget import get_mask_account, get_date


# Фикстура для генерации тестовых данных для маскирования карт и счетов
@pytest.fixture
def card_and_account_test_data():
    """
    Фикстура с примерами разных данных для тестирования mask_account_card.
    """
    return [
        {"input": "Карта 1234-5678-9012-3456", "expected": "**** **** ****3456", "is_card": True},
        {"input": "Cчет: 12345678", "expected": "**5678", "is_card": False},
        {"input": "Карта ABCD-EFGH", "expected": None, "is_card": True},  # Ошибка (нет цифр)
        {"input": "Cчет: ABCD", "expected": None, "is_card": False},  # Ошибка (нет цифр)
        {"input": "Карта 1234", "expected": None, "is_card": True},  # Короткий номер карты
        {"input": "Cчет: 12", "expected": None, "is_card": False},  # Короткий номер счета
        {"input": "Карта", "expected": None},  # Никаких цифр вообще
    ]


# Фикстура для тестирования разных форматов даты
@pytest.fixture
def date_test_data():
    """
    Фикстура с примерами корректных и некорректных данных для тестирования get_date.
    """
    return [
        {"input": "2023 01. 15", "expected": "15.01.2023"},
        {"input": "2021 12. 31", "expected": "31.12.2021"},
        {"input": "2022 02. 29", "expected": None},  # Некорректная дата
        {"input": "15-01-2023", "expected": None},  # Неверный формат
        {"input": "", "expected": None},  # Пустая строка
        {"input": "2023 01. 15 12:00", "expected": None},  # Дополнительные данные
    ]


# Тесты для mask_account_card
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


# Тесты для get_date
def test_get_date(date_test_data):
    """
    Тестирование функции get_date на основе тестовых данных.
    """
    for data in date_test_data:
        input_date = data["input"]
        expected = data["expected"]

        if expected is None:
            # Ожидание исключения при ошибочных данных
            with pytest.raises(ValueError):
                get_date(input_date)
        else:
            # Проверка результата
            result = get_date(input_date)
            assert result == expected
