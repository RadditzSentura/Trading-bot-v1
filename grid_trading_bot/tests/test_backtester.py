# tests/test_backtester.py

import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.backtester import Backtester
from src.strategies.default_strategy import DefaultStrategy

def test_run_backtest():
    # Mock components
    grid_calculator = MagicMock()
    grid_calculator.calculate_static_grids.return_value = {
        'prices': [100, 110, 120],
        'quantities': [1, 1, 1]
    }

    order_manager = MagicMock()
    tech_indicators = MagicMock()
    performance_tracker = MagicMock()

    # Mock strategy
    strategy = MagicMock(spec=DefaultStrategy)
    strategy.decide.return_value = [
        {'side': 'buy', 'amount': 1, 'price': 100},
        {'side': 'sell', 'amount': 1, 'price': 101, 'profit': 1.0}
    ]

    # Sample historical data
    historical_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2021-01-01', periods=3, freq='H'),
        'price': [95, 115, 125]
    })

    # Initialize Backtester
    backtester = Backtester(grid_calculator, order_manager, tech_indicators, performance_tracker, strategy)

    # Run backtest
    backtester.run_backtest(historical_data)

    # Assertions
    grid_calculator.calculate_static_grids.assert_called_once()
    strategy.decide.assert_called()
    assert performance_tracker.record_trade.call_count == 2  # Buy and Sell
    performance_tracker.record_trade.assert_any_call(-100)  # Buying reduces profit
    performance_tracker.record_trade.assert_any_call(1.0)   # Selling increases profit