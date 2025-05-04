def mask_card_number(card_number):
    """Маскирует номер карты (XXXX XXXX XXXX 1234)"""
    if not card_number or len(card_number) < 4:
        return card_number
    return '**** **** **** ' + card_number[-4:]

def mask_account(account):
    """Маскирует номер счета (**1234)"""
    if not account or len(account) < 4:
        return account
    return '**' + account[-4:]