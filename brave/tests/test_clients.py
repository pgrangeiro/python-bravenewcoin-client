import pytz
import vcr

from datetime import datetime
from freezegun import freeze_time
from unittest import TestCase
from unittest.mock import Mock, patch

from brave.clients import BaseClient, ExchangeClient, MarketClient, SpotPriceClient
from brave.exceptions import BraveAPIConnectionError
from brave.parsers import NullableParser


class BaseClientTestCase(TestCase):

    def setUp(self):
        self.stub_client_class = type('StubClass', (BaseClient, ), {'PATH_URL': 'path'})
        self.client = self.stub_client_class(1, ('key', 'token'))

    def test_initializes_instance_correctly(self):
        self.assertEqual(NullableParser, self.client.parser)
        self.assertEqual(1, self.client.customer)
        self.assertEqual(('key', 'token'), self.client.credentials)
        self.assertEqual(
            'https://api.bravenewcoin.com/', self.client.BASE_URL
        )
    def test_initializes_instance_with_parser_correctly(self):
        client = self.stub_client_class(
            1, ('key', 'token'), 3
        )
        self.assertEqual(1, client.customer)
        self.assertEqual(('key', 'token'), self.client.credentials)
        self.assertEqual(3, client.parser)
        self.assertEqual('https://api.bravenewcoin.com/', client.BASE_URL)

    def test_build_customer_url_correctly(self):
        url = self.client.build_customer_base_url()
        self.assertEqual('https://api.bravenewcoin.com/1/', url)

    def test_property_url_returns_correct_data(self):
        self.assertEqual(
            'https://api.bravenewcoin.com/1/path/', self.client.url
        )

    def test_build_headers_correctly(self):
        expected = {'key': 'token', 'Accept': 'application/json'}
        self.assertEqual(expected, self.client.headers)

    @patch('brave.clients.requests')
    def test_get_calls_request_correctly(self, m_request):
        self.client.parser = Mock(NullableParser)
        self.client.parser.parse.return_value = {'1': 1}

        data = self.client.get(coin='btc', show='usd')

        m_request.get.assert_called_once_with(
            self.client.url,
            params={'coin': 'btc', 'show': 'usd'},
            headers={
                'key': 'token',
                'Accept': 'application/json',
            },
        )
        self.client.parser.parse.assert_called_once_with(m_request.get().json())
        self.assertEqual({'1': 1}, data)


class SpotPriceClientTestCase(TestCase):

    def setUp(self):
        self.client = SpotPriceClient('customer', ('Key', 'Token'))

    def test_initializes_instance_correctly(self):
        self.assertIsInstance(self.client, BaseClient)
        self.assertEqual('customer', self.client.customer)
        self.assertEqual(
            ('Key', 'Token'), self.client.credentials
        )
        self.assertEqual('ticker', self.client.PATH_URL)

    @patch('brave.clients.requests')
    def test_get_calls_request_correctly(self, m_request):
        self.client.get('btc')

        m_request.get.assert_called_once_with(
            self.client.url,
            params={'coin': 'btc', 'show': 'usd'},
            headers={
                'Key': 'Token',
                'Accept': 'application/json',
            },
        )

    @vcr.use_cassette()
    def test_get_do_request_to_brave_api_correctly(self):
        data = self.client.get('btc')
        self.assertTrue(data['success'])

    @vcr.use_cassette()
    def test_get_raises_exception_when_request_not_successful(self):
        self.assertRaises(BraveAPIConnectionError, self.client.get, 'btc')


class ExchangeClientTestCase(TestCase):

    def setUp(self):
        self.client = ExchangeClient('customer', ('Key', 'Token'))

    def test_initializes_instance_correctly(self):
        self.assertIsInstance(self.client, BaseClient)
        self.assertEqual('customer', self.client.customer)
        self.assertEqual(
            ('Key', 'Token'), self.client.credentials
        )
        self.assertEqual('mwa-historic', self.client.PATH_URL)

    @freeze_time('2018-01-01 12:01')
    @patch('brave.clients.requests')
    def test_get_calls_request_correctly(self, m_request):
        self.client.get('btc')

        expected_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        m_request.get.assert_called_once_with(
            self.client.url,
            params={
                'coin': 'btc',
                'from': expected_datetime.timestamp(),
                'market': 'usd'
            },
            headers={
                'Key': 'Token',
                'Accept': 'application/json',
            },
        )

    @patch('brave.clients.requests')
    def test_get_with_extra_params_calls_request_correctly(self, m_request):
        start_at = datetime(2018, 1, 1, 12, 1, tzinfo=pytz.utc)
        end_at = datetime(2018, 1, 2, 9, tzinfo=pytz.utc)
        self.client.get('btc', start_at, end_at)

        m_request.get.assert_called_once_with(
            self.client.url,
            params={
                'coin': 'btc',
                'from': start_at.timestamp(),
                'to': end_at.timestamp(),
                'market': 'usd'
            },
            headers={
                'Key': 'Token',
                'Accept': 'application/json',
            },
        )

    @freeze_time('2018-01-01 12:01')
    @vcr.use_cassette()
    def test_exchange_get_do_request_to_brave_api_correctly(self):
        data = self.client.get('btc')
        self.assertTrue(data['success'])

    @freeze_time('2018-01-01 12:01')
    @vcr.use_cassette()
    def test_exchange_get_raises_exception_when_request_not_successful(self):
        self.assertRaises(BraveAPIConnectionError, self.client.get, 'btc')


class MarketClientTestCase(TestCase):

    def setUp(self):
        self.client = MarketClient('customer', ('Key', 'Token'))

    def test_initializes_instance_correctly(self):
        self.assertIsInstance(self.client, BaseClient)
        self.assertEqual('customer', self.client.customer)
        self.assertEqual(
            ('Key', 'Token'), self.client.credentials
        )
        self.assertEqual('market-table', self.client.PATH_URL)

    @vcr.use_cassette()
    def test_market_get_do_request_to_brave_api_correctly(self):
        data = self.client.get()
        self.assertTrue(data['success'])

    @vcr.use_cassette()
    def test_market_get_raises_exception_when_request_not_successful(self):
        self.assertRaises(BraveAPIConnectionError, self.client.get)
