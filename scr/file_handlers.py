import csv
import openpyxl
from datetime import datetime
from typing import List, Dict, Union, Optional
from enum import Enum


class TransactionState(Enum):
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELED"
    PENDING = "PENDING"


class TransactionType(Enum):
    CARD_TO_CARD = "Перевод с карты на карту"
    ACCOUNT_TO_ACCOUNT = "Перевод со счета на счет"
    CARD_TO_ACCOUNT = "Перевод организации"
    DEPOSIT_OPENING = "Открытие вклада"


class FinancialTransaction:
    def __init__(self, transaction_data: Dict[str, Union[str, float]]):
        self.id = transaction_data.get('id', '')
        self.state = self._parse_state(transaction_data.get('state', ''))
        self.date = self._parse_date(transaction_data.get('date', ''))
        self.amount = float(transaction_data.get('amount', 0))
        self.currency_name = transaction_data.get('currency_name', '')
        self.currency_code = transaction_data.get('currency_code', '')
        self.source = transaction_data.get('from', '')
        self.destination = transaction_data.get('to', '')
        self.description = transaction_data.get('description', '')
        self.type = self._determine_transaction_type()

    def _parse_state(self, state_str: str) -> Optional[TransactionState]:
        """Parse transaction state string into TransactionState enum"""
        if not state_str:
            return None
        try:
            return TransactionState[state_str.upper()]
        except KeyError:
            return None

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string into datetime object"""
        if not date_str:
            return None

        try:
            for fmt in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M:%S'):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        except (ValueError, TypeError):
            return None

    def _determine_transaction_type(self) -> Optional[TransactionType]:
        """Determine transaction type based on description and account patterns"""
        if not self.description:
            return None

        description_lower = self.description.lower()

        if "карты на карту" in description_lower:
            return TransactionType.CARD_TO_CARD
        elif "счета на счет" in description_lower:
            return TransactionType.ACCOUNT_TO_ACCOUNT
        elif "организации" in description_lower or (
                "счет" in self.source.lower() and "карт" not in self.destination.lower()):
            return TransactionType.CARD_TO_ACCOUNT
        elif "вклад" in description_lower or (not self.source and "счет" in self.destination.lower()):
            return TransactionType.DEPOSIT_OPENING
        return None

    def is_card_number(self, account: str) -> bool:
        """Check if account string is a card number"""
        if not account:
            return False
        return any(word in account.lower() for word in ["visa", "mastercard", "american express", "discover"])

    def get_card_number(self, account: str) -> Optional[str]:
        """Extract card number from account string"""
        if not self.is_card_number(account):
            return None
        parts = account.split()
        return parts[-1] if len(parts) > 1 else None

    def get_account_number(self, account: str) -> Optional[str]:
        """Extract account number from account string"""
        if not account:
            return None
        if "счет" in account.lower():
            parts = account.split()
            return parts[-1] if len(parts) > 1 else None
        return None

    def __repr__(self):
        return (f"FinancialTransaction(id={self.id}, state={self.state.name if self.state else 'UNKNOWN'}, "
                f"date={self.date}, amount={self.amount} {self.currency_code}, type={self.type.name if self.type else 'UNKNOWN'})")


class FinancialDataAnalyzer:
    def __init__(self, transactions: List[FinancialTransaction]):
        self.transactions = transactions

    def filter_by_state(self, state: TransactionState) -> List[FinancialTransaction]:
        """Filter transactions by state"""
        return [t for t in self.transactions if t.state == state]

    def filter_by_type(self, transaction_type: TransactionType) -> List[FinancialTransaction]:
        """Filter transactions by type"""
        return [t for t in self.transactions if t.type == transaction_type]

    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> List[FinancialTransaction]:
        """Filter transactions within date range"""
        return [t for t in self.transactions if t.date and start_date <= t.date <= end_date]

    def get_total_amount_by_currency(self) -> Dict[str, float]:
        """Calculate total amount for each currency"""
        totals = {}
        for t in self.transactions:
            if t.currency_code not in totals:
                totals[t.currency_code] = 0.0
            totals[t.currency_code] += t.amount
        return totals

    def get_transactions_by_card(self, card_last_digits: str) -> List[FinancialTransaction]:
        """Get all transactions for a specific card (last 4 digits)"""
        return [t for t in self.transactions
                if (t.is_card_number(t.source) and t.get_card_number(t.source)[-4:] == card_last_digits) or (t.is_card_number(t.destination) and t.get_card_number(t.destination)[-4:] == card_last_digits)]

    def get_largest_transactions(self, n: int = 5) -> List[FinancialTransaction]:
        """Get the n largest transactions by amount"""
        return sorted(self.transactions, key=lambda x: x.amount, reverse=True)[:n]

    def get_most_active_currencies(self, n: int = 5) -> Dict[str, int]:
        """Get the n most frequently used currencies"""
        currency_counts = {}
        for t in self.transactions:
            if t.currency_code not in currency_counts:
                currency_counts[t.currency_code] = 0
            currency_counts[t.currency_code] += 1
        return dict(sorted(currency_counts.items(), key=lambda item: item[1], reverse=True)[:n])


class FinancialDataReader:
    @staticmethod
    def read_transactions(file_path: str) -> List[FinancialTransaction]:
        """Read financial transactions from file (CSV or XLSX)"""
        if file_path.endswith('.csv'):
            return FinancialDataReader._read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return FinancialDataReader._read_xlsx(file_path)
        else:
            raise ValueError("Unsupported file format. Only CSV and XLSX are supported.")

    @staticmethod
    def _read_csv(file_path: str) -> List[FinancialTransaction]:
        """Read data from CSV file"""
        transactions = []

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                row = {k.lower(): v for k, v in row.items()}
                transactions.append(FinancialTransaction(row))

        return transactions

    @staticmethod
    def _read_xlsx(file_path: str) -> List[FinancialTransaction]:
        """Read data from XLSX file"""
        transactions = []

        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        headers = []
        for cell in sheet[1]:
            headers.append(cell.value.lower() if cell.value else '')

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {}
            for header, value in zip(headers, row):
                if header:
                    row_data[header] = str(value) if value is not None else ''

            transactions.append(FinancialTransaction(row_data))

        return transactions


# Example usage with analysis
if __name__ == "__main__":
    try:
        # Read transactions from Excel file
        transactions = FinancialDataReader.read_transactions("transactions_excel.xlsx")
        print(f"Successfully read {len(transactions)} transactions")

        # Create analyzer
        analyzer = FinancialDataAnalyzer(transactions)

        # Example analyses
        print("\n=== Executed Transactions ===")
        executed = analyzer.filter_by_state(TransactionState.EXECUTED)
        print(f"Count: {len(executed)}")

        print("\n=== Card-to-Card Transactions ===")
        card_transfers = analyzer.filter_by_type(TransactionType.CARD_TO_CARD)
        print(f"Count: {len(card_transfers)}")
        for t in card_transfers[:3]:
            print(t)

        print("\n=== Total Amount by Currency ===")
        totals = analyzer.get_total_amount_by_currency()
        for currency, amount in totals.items():
            print(f"{currency}: {amount:.2f}")

        print("\n=== Largest 5 Transactions ===")
        largest = analyzer.get_largest_transactions(5)
        for t in largest:
            print(f"{t.amount} {t.currency_code} on {t.date}")

        print("\n=== Most Active Currencies ===")
        active_currencies = analyzer.get_most_active_currencies(5)
        for currency, count in active_currencies.items():
            print(f"{currency}: {count} transactions")

        # Example: Get transactions for a specific card (last 4 digits)
        print("\n=== Transactions for Card ending with 1439 ===")
        card_transactions = analyzer.get_transactions_by_card("1439")
        print(f"Found {len(card_transactions)} transactions")
        for t in card_transactions[:3]:
            print(t)

    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {e}")
