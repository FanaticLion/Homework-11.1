def process_transactions(transactions):
    """Обрабатывает список транзакций"""
    processed = []
    total = 0.0

    for tx in transactions:
        amount = float(tx.get('amount', 0))
        processed.append(tx)
        total += amount

    return {
        'transactions': processed,
        'total_amount': total,
        'count': len(processed)
    }