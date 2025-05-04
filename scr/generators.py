import random
from datetime import datetime, timedelta
from typing import List, Dict
from masks import mask_card_number, mask_account


def generate_fake_card_number() -> str:
    """Генерирует случайный номер карты"""
    return f"{random.randint(4000, 4999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"


def generate_fake_account() -> str:
    """Генерирует случайный номер счета"""
    return f"40817{random.randint(10, 99)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"


def generate_test_transactions(count: int = 10) -> List[Dict]:
    """Генерирует список тестовых транзакций"""
    transactions = []
    categories = ["Еда", "Транспорт", "Развлечения", "Одежда", "Жилье"]

    for i in range(1, count + 1):
        card_num = generate_fake_card_number()
        tx_date = (datetime.now() - timedelta(days=random.randint(0, 365))).date()

        transactions.append({
            'transaction_id': f"T{i:05d}",
            'date': tx_date.isoformat(),
            'amount': round(random.uniform(50, 5000), 2),
            'currency': "RUB",
            'category': random.choice(categories),
            'description': f"Платеж #{i}",
            'card_number': card_num,
            'masked_card': mask_card_number(card_num),
            'account': generate_fake_account(),
            'status': random.choice(["completed", "pending", "failed"])
        })

    return transactions