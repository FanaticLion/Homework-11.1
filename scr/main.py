from file_handlers import FileHandler
from processing import process_transactions
from utils import format_transaction
import sys

def main():
    print("""Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла""")

    while True:
        choice = input("Пользователь: ").strip()
        if choice in ("1", "2", "3"):
            break
        print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")

    file_path = input("Введите путь к файлу: ")

    try:
        handler = FileHandler()
        if choice == "1":
            transactions = handler.load_json(file_path)
        elif choice == "2":
            transactions = handler.load_csv(file_path)
        else:
            transactions = handler.load_xlsx(file_path)

        result = process_transactions(transactions)
        display_transactions(result['transactions'])
        print(f"\nИтого: {len(result['transactions'])} транзакций на сумму {result['total_amount']:.2f} руб.")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

def display_transactions(transactions):
    print("\nСписок транзакций:")
    for i, tx in enumerate(transactions, 1):
        formatted = format_transaction(tx)
        print(f"{i}. {formatted['date']} - {formatted['description']}: {formatted['amount']}")

if __name__ == "__main__":
    main()