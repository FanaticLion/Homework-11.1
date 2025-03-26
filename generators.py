# Python code for generators.py

def filter_by_currency(data_list, currency):
    """
    Filters a list of dictionaries, returning an iterator over dictionaries
    that have a specific 'currency' key value.

    Args:
        data_list (list): List of dictionaries to filter.
        currency (str): The currency to filter by.

    Returns:
        iterator: An iterator of dictionaries that match the given currency.
    """
    if not isinstance(data_list, list):
        raise ValueError("data_list must be a list of dictionaries.")

    for item in data_list:
        if not isinstance(item, dict):
            raise ValueError("All elements in data_list must be dictionaries.")
        if item.get("currency") == currency:
            yield item