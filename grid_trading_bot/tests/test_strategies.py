# tests/test_strategies.py

import pytest
from src.strategies.default_strategy import DefaultStrategy

def test_default_strategy_buy_decision():
    parameters = {
        'volatility_period': 14,
        'rsi_threshold': 70,
        'macd_fast_period': 12,
        'macd_slow_period': 26,
        'macd_signal_period': 9
    }
    strategy = DefaultStrategy(parameters)
    current_price = 95
    grids = [100, 110, 120]
    quantities = [1, 1, 1]
    data = {
        'rsi': 65,
        'macd': {'histogram': [0.5, 0.3]}
    }
    decisions = strategy.decide(current_price, grids, quantities, data)
    assert len(decisions) == 1
    assert decisions[0]['side'] == 'buy'
    assert decisions[0]['amount'] == 1
    assert decisions[0]['price'] == 100

def test_default_strategy_sell_decision():
    parameters = {
        'volatility_period': 14,
        'rsi_threshold': 70,
        'macd_fast_period': 12,
        'macd_slow_period': 26,
        'macd_signal_period': 9
    }
    strategy = DefaultStrategy(parameters)
    current_price = 115
    grids = [100, 110, 120]
    quantities = [1, 1, 1]
    data = {
        'rsi': 75,
        'macd': {'histogram': [0.5, 0.3]}
    }
    decisions = strategy.decide(current_price, grids, quantities, data)
    assert len(decisions) == 1
    assert decisions[0]['side'] == 'sell'
    assert decisions[0]['amount'] == 1
    assert decisions[0]['price'] == 110 * 1.01
    assert decisions[0]['profit'] == 1.0

def test_default_strategy_no_decision():
    parameters = {
        'volatility_period': 14,
        'rsi_threshold': 70,
        'macd_fast_period': 12,
        'macd_slow_period': 26,
        'macd_signal_period': 9
    }
    strategy = DefaultStrategy(parameters)
    current_price = 125
    grids = [100, 110, 120]
    quantities = [1, 1, 1]
    data = {
        'rsi': 80,
        'macd': {'histogram': [-0.2, -0.1]}
    }
    decisions = strategy.decide(current_price, grids, quantities, data)
    assert len(decisions) == 0