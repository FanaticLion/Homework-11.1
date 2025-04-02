from typing import List, Dict


def get_mask_card_number(card_number: str) -> str:
    card_str = str(card_number)
    if not card_str.isdigit():
        raise ValueError("Card number must contain only digits.")
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр.")
    return f"**** **** ****{card_str[-4:]}"


def get_mask_account(account_number: str) -> str:
    account_str = str(account_number)
    if not account_str.isdigit():
        raise ValueError("Account number must contain only digits.")
    if len(account_str) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры.")
    return f"**{account_str[-4:]}"


def filter_by_state(transactions, state="EXECUTED") -> list:
    filtered_transactions = [transaction for transaction in transactions if transaction.get('state') == state]
    return filtered_transactions


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    return sorted(transactions, key=lambda x: x['date'], reverse=reverse)


if __name__ == "__main__":
    result = sort_by_date([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ])
    print(result)
