import requests
from typing import Optional, List, Dict


class BankAPI:
    def __init__(self, base_url: str = "https://api.example-bank.com/v1"):
        self.base_url = base_url

    def get_transactions(self, account_id: str, from_date: str, to_date: str) -> Optional[List[Dict]]:
        endpoint = f"{self.base_url}/accounts/{account_id}/transactions"
        params = {
            'from': from_date,
            'to': to_date
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json().get('transactions', [])
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None