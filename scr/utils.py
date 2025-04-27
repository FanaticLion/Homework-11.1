import re
from collections import Counter
from typing import List, Dict, Any
import logging
from pathlib import Path


def setup_logger():
    """Настройка логгера для модуля"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger('transaction_utils')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    handler = logging.FileHandler(
        filename=logs_dir / "transactions.log",
        mode='w',
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)
    return logger


utils_logger = setup_logger()


def filter_transactions(transactions: List[Dict[str, Any]],
                        search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по строке поиска в описании"""
    try:
        utils_logger.debug(f"Фильтрация по строке: '{search_string}'")
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        return [t for t in transactions
                if pattern.search(t.get('description', ''))]
    except Exception as e:
        utils_logger.error(f"Ошибка фильтрации: {str(e)}")
        return []


def count_transactions(transactions: List[Dict[str, Any]],
                       categories: Dict[str, List[str]]) -> Dict[str, int]:
    """Подсчитывает транзакции по категориям"""
    try:
        utils_logger.debug("Подсчет транзакций по категориям")
        category_counts = Counter()

        for transaction in transactions:
            description = transaction.get('description', '').lower()
            for category, keywords in categories.items():
                if any(kw.lower() in description for kw in keywords):
                    category_counts[category] += 1
                    break

        return dict(category_counts)
    except Exception as e:
        utils_logger.error(f"Ошибка подсчета: {str(e)}")
        return {}