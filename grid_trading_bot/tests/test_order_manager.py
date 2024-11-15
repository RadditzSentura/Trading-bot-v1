# tests/test_order_manager.py

import pytest
from src.order_manager import OrderManager

def test_place_limit_order(mock_exchange):
    order_manager = OrderManager(exchange=mock_exchange)
    order = order_manager.place_limit_order(symbol='BTC/USD', side='buy', amount=0.01, price=15000)
    assert order['id'] == 'test_order_id'
    assert order['status'] == 'open'
    mock_exchange.create_limit_order.assert_called_once_with('BTC/USD', 'buy', 0.01, 15000)

def test_cancel_all_orders(mock_exchange):
    order_manager = OrderManager(exchange=mock_exchange)
    order_manager.cancel_all_orders(symbol='BTC/USD')
    assert mock_exchange.cancel_order.call_count == 2
    mock_exchange.cancel_order.assert_any_call('order1')
    mock_exchange.cancel_order.assert_any_call('order2')

def test_get_active_orders(mock_exchange):
    order_manager = OrderManager(exchange=mock_exchange)
    orders = order_manager.get_active_orders(symbol='BTC/USD')
    assert len(orders) == 2
    mock_exchange.get_active_orders.assert_called_once_with('BTC/USD')