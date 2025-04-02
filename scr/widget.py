import re
from scr.masks import get_mask_card_number, get_mask_account
from datetime import datetime  #


def mask_account_card(card_number: str) -> str:
    """Функция, которая принимает счет и номер карты и возвращает зашифрованный"""
    # Найти только цифровые символы
    only_numbers = re.findall(r"\d+", card_number)
    if not only_numbers:
        raise ValueError("В строке отсутствуют цифры.")

    str_only_numbers = "".join(only_numbers)
    if "Cчет" in card_number:
        return get_mask_account(str_only_numbers)
    else:
        return get_mask_card_number(str_only_numbers)


def get_date(input_date: str) -> str:
    """
    Преобразует строку даты в требуемый формат 'дд.мм.гггг'.
    Если формат неверный, выбрасывает ValueError.
    """
    try:
        # Определим правильный формат даты
        parsed_date = datetime.strptime(input_date.strip(), "%Y %m. %d")
        # Вернем дату в желаемом формате
        return parsed_date.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        # Если дата некорректна
        raise ValueError("Некорректный формат даты или неверные данные")
