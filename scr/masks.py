import logging
from typing import Union

# Настройка логгера для модуля masks
masks_logger = logging.getLogger('masks')
masks_logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# Создаем file handler
file_handler = logging.FileHandler('masks.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем formatter
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
masks_logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Возвращает маску номера карты в формате XXXX XX** **** XXXX

    :param card_number: Номер карты (строка или число)
    :return: Маскированный номер карты
    """
    try:
        card_str = str(card_number).strip()
        masks_logger.debug(f"Начало обработки номера карты: {card_str}")

        # Проверка на пустую строку
        if not card_str:
            error_msg = "Номер карты не может быть пустым"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверка на минимальную длину
        if len(card_str) < 16:
            error_msg = f"Номер карты слишком короткий: {len(card_str)} символов"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверка на цифры
        if not card_str.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматирование маски
        masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        masks_logger.info(f"Успешно сформирована маска для карты: {masked_number}")
        return masked_number


    except Exception as card_error:  # Уникальное имя

        masks_logger.critical(f"Критическая ошибка при обработке карты: {str(card_error)}")

        raise


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера счёта в формате **XXXX

    :param account_number: Номер счёта (строка)
    :return: Маскированный номер счёта
    """
    try:
        masks_logger.debug(f"Начало обработки номера счёта: {account_number}")

        # Проверка на тип
        if not isinstance(account_number, str):
            error_msg = "Номер счёта должен быть строкой"
            masks_logger.error(error_msg)
            raise TypeError(error_msg)

        account_number = account_number.strip()

        # Проверка на пустую строку
        if not account_number:
            error_msg = "Номер счёта не может быть пустым"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверка на цифры
        if not account_number.isdigit():
            error_msg = "Номер счёта должен содержать только цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверка длины
        if len(account_number) < 4:
            error_msg = "Номер счёта должен содержать минимум 4 цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Формирование маски
        if len(account_number) <= 18:
            masked_account = "**" + account_number[-4:]
        else:
            masked_account = "**" + account_number[-6:]

        masks_logger.info(f"Успешно сформирована маска для счёта: {masked_account}")
        return masked_account


    except Exception as account_error:  # Уникальное имя

        masks_logger.critical(f"Критическая ошибка при обработке счёта: {str(account_error)}")

        raise

# Пример использования
if __name__ == "__main__":
    try:
        print(get_mask_card_number("1234567890123456"))  # 1234 56** **** 3456
        print(get_mask_account("1234567890"))  # **7890
    except Exception as e:
        print(f"Ошибка: {e}")