# tests/test_exchange_interface.py

import pytest
from src.exchange_interface import ExchangeInterface

def test_get_current_price(mock_exchange):
    price = mock_exchange.get_current_price('BTC/USD')
    assert price == 100.0
    mock_exchange.fetch_ticker.assert_called_once_with('BTC/USD')

def test_create_limit_order(mock_exchange):
    order = mock_exchange.create_limit_order('BTC/USD', 'buy', 0.01, 15000)
    assert order['id'] == 'test_order_id'
    assert order['status'] == 'open'
    mock_exchange.create_limit_order.assert_called_once_with('BTC/USD', 'buy', 0.01, 15000)

def test_cancel_order(mock_exchange):
    result = mock_exchange.cancel_order('order1')
    assert result is True
    mock_exchange.cancel_order.assert_called_once_with('order1')

def test_get_active_orders(mock_exchange):
    orders = mock_exchange.get_active_orders('BTC/USD')
    assert len(orders) == 2
    mock_exchange.fetch_open_orders.assert_called_once_with('BTC/USD')