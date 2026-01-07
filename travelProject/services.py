import requests
from decimal import Decimal
from django.conf import settings

def fetch_currency_rates():
    """Получает курсы валют с внешнего API.
    
    Returns:
        dict: Словарь с курсами валют относительно RUB.
              Пример: {'USD': 90.5, 'EUR': 98.2}
    """
    try:
        url = 'https://api.exchangerate-api.com/v4/latest/RUB'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        rates = {}
        for code, rate in data.get('rates', {}).items():
            if rate > 0:
                rates[code] = Decimal(1 / rate)
                
        return rates
    except Exception as e:
        print(f"Error fetching currency rates: {e}")
        return {}
