import pytz
import requests
from abc import ABC
from datetime import datetime

from brave.exceptions import BraveAPIConnectionError
from brave.parsers import NullableParser


class BaseClient(ABC):

    BASE_URL = 'https://api.bravenewcoin.com/'
    PATH_URL = ''

    def __init__(self, customer, credentials, parser=None):
        self.customer = customer
        self.credentials = credentials
        self.parser = parser or NullableParser

    def build_customer_base_url(self):
        return f'{self.BASE_URL}{self.customer}/'

    @property
    def url(self):
        return f'{self.build_customer_base_url()}{self.PATH_URL}/'

    @property
    def headers(self):
        return {
            self.credentials[0]: self.credentials[1],
            'Accept': 'application/json',
        }

    def get(self, **kwargs):
        response = requests.get(
            self.url, params=kwargs, headers=self.headers
        )
        response.raise_for_status()

        data = response.json()
        if not data['success']:
            raise BraveAPIConnectionError(data['error'])

        return self.parser.parse(response.json())


class SpotPriceClient(BaseClient):

    PATH_URL = 'ticker'

    def get(self, ticker, currency='usd'):
        params = {
            'coin': ticker,
            'show': currency,
        }
        return super().get(**params)


class ExchangeClient(BaseClient):

    PATH_URL = 'mwa-historic'

    def get(self, ticker, start_at=None, end_at=None, currency='usd'):
        start_at = start_at or datetime.utcnow().replace(tzinfo=pytz.utc)
        start_at = start_at.timestamp()

        params = {
            'coin': ticker,
            'from': start_at,
            'market': currency,
        }
        if end_at:
            params['to'] = end_at.timestamp()

        return super().get(**params)


class MarketClient(BaseClient):

    PATH_URL = 'market-table'

    def get(self, days=1):
        params = {
            'days': days,
        }
        return super().get(**params)
