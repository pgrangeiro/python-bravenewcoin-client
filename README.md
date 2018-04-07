# Python Brave New Coin Client
[![Build Status](https://travis-ci.org/pgrangeiro/python-bravenewcoin-client.svg?branch=master)](https://travis-ci.org/pgrangeiro/python-bravenewcoin-client)

A Python library to connect with [Brave New Coin](https://bravenewcoin.com) APIs.

Supported APIs:
- [Ticker Price](https://market.mashape.com/bravenewcoin/digital-currency-tickers#ticker)
- [MWA Historic Data](https://market.mashape.com/BraveNewCoin/digital-currency-ex-rates#mwa-historic-exchange-rates)
- [Market Cap Table Data](https://bravenewcoin.com/market-cap/)


# Install
```
pip install
```


# Tests
```
tox
```


# Usage

## Get crypto coin latest quotes

Return the latest quote for crypto coin.

Parameters:
- Ticker: The crypto coin ticker. Type: String.
- Currency[optional]: The crypto coin value converted to currency. Type: String. Default: USD.

```
>>> from brave.clients import SpotPriceClient
>>> client = SpotPriceClient('customer', ('BraveNewCoin-API-Key', 'Token'))
>>> client.get('btc')
{'success': True, 'source': 'BraveNewCoin', 'time_stamp': 1523066461, 'utc...
```

## Get crypto coin exchange rates

Return the historic exchange data for crypto coin.

Parameters:
- Ticker: The crypto coin ticker. Type: String.
- Start Date[optional]: Get historic data from start date. Type: Datetime. Default: Today.
- End Date[optional]: Get historic data until end date. Type: Datetime. Default: Today.
- Currency[optional]: The crypto coin value converted to currency. Type: String. Default: USD.

```
>>> from brave.clients import ExchangeClient
>>> client = ExchangeClient('customer', ('BraveNewCoin-API-Key', 'Token'))
>>> client.get('btc')
{'success': True, 'source': 'BraveNewCoin', 'time_stamp': 1523066820, 'utc...
```

## Get crypto coins market capitalization

Return the market capitalization data for all crypto coins tracked by Brave New Coin.

Parameters:
- Days[optional]: Get market cap data for a number of days. Type: Integer. Default: 1.

```
>>> from brave.clients import MarketClient
>>> client = MarketClient('customer', ('BraveNewCoin-API-Key', 'Token'))
>>> client.get()
{'success': True, 'source': 'BraveNewCoin', 'endpoint': 'market-table', 'r...
```
