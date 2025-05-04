from datetime import datetime


def format_transaction(transaction):
    """Форматирует транзакцию для отображения"""
    date = transaction.get('date', '')
    if date:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
        except ValueError:
            pass

    return {
        'date': date,
        'description': transaction.get('description', 'Без описания'),
        'amount': f"{transaction.get('amount', 0):.2f} руб."
    }
