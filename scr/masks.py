def get_mask_card_number(card_number: str) -> str:
    card_str = str(card_number)

    # Проверка на пустую строку
    if not card_str.strip():
        raise ValueError("Card number is empty")

    # Проверка на минимальную длину номера карты
    if len(card_str) < 16:
        raise ValueError("Card number is too short")

    # Проверка на то, что номер карты состоит только из цифр
    if not card_str.isdigit():
        raise ValueError("Card number must contain only digits.")

    # Формирование маски
    return f"{card_str[:4]} {card_str[4:6]} ** **** **** {card_str[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Создать маску для номера счёта."""
    # Проверка на тип входного значения
    if not isinstance(account_number, str):
        raise TypeError("Номер счёта должен быть строкой.")

    # Проверка на пустую строку или строку из пробелов
    if not account_number.strip():
        raise ValueError("Номер счёта должен содержать минимум 4 цифры.")

    # Проверка, что строка состоит только из цифр
    if not account_number.isdigit():
        raise ValueError("Содержит недопустимые символы.")

    # Проверка на минимальное количество символов
    if len(account_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры.")

    # Маскирование
    if len(account_number) <= 10:  # Если длина строки не превышает 10
        return "****" + account_number[-4:]
    else:  # Если длина строки больше 10
        return "****" + account_number[-6:]
