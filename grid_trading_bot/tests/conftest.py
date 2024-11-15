# tests/conftest.py

import pytest
from unittest.mock import MagicMock
from src.exchange_interface import ExchangeInterface

@pytest.fixture
def mock_exchange():
    exchange = MagicMock(spec=ExchangeInterface)
    exchange.create_limit_order.return_value = {'id': 'test_order_id', 'status': 'open'}
    exchange.fetch_open_orders.return_value = [{'id': 'order1'}, {'id': 'order2'}]
    exchange.fetch_ticker.return_value = {'last': 100.0}
    exchange.exchange.fetch_ohlcv.return_value = [
        [1609459200000, 29000, 29500, 28500, 29000, 10],
        [1609462800000, 29000, 29500, 28500, 29000, 10],
        # Add more mock OHLCV data as needed
    ]
    return exchange