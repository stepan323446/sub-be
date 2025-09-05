import requests
from django.core.cache import cache
from rest_framework.exceptions import server_error
from project.settings_context import EXCHANGE_RATE_KEY
from .models import Currency

CURRENCY_CACHE_TIME = 60 * 60 * 6

def update_currencies():
    # Get current currencies in local db
    currencies = list(Currency.objects.all())

    # Get currencies by external service api
    exchange_response = requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_KEY}/latest/USD')
    if not exchange_response.ok:
        raise Exception('Unable to retrieve exchange rates')
    
    response_json = exchange_response.json()
    exchange_rates: dict = response_json['conversion_rates']

    # Update exist currencies
    for currency in currencies:
        if hasattr(currency, 'code'):
            rate = exchange_rates.pop(currency.code, None)
            if rate is not None:
                currency.conversion_rate = rate
            else:
                currency.delete()

    Currency.objects.bulk_update(currencies, ['conversion_rate'])

    # Add new currencies
    new_currencies = list()
    for curr_code, curr_rate in exchange_rates.items():
        currency = Currency(code=curr_code, conversion_rate=curr_rate)
        new_currencies.append(currency)

    Currency.objects.bulk_create(new_currencies)

    currencies += new_currencies
    cache.set("cached_currencies", currencies, timeout=CURRENCY_CACHE_TIME)

    return currencies

def get_cached_currencies():
    currencies = cache.get("cached_currencies")

    if not currencies:
        currencies = update_currencies()
        cache.set("cached_currencies", currencies, timeout=CURRENCY_CACHE_TIME)

    return currencies
