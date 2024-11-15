# tests/test_technical_indicators.py

import pytest
from src.technical_indicators import TechnicalIndicators

def test_calculate_rsi():
    ti = TechnicalIndicators()
    data = [44, 45, 46, 47, 46, 45, 44, 43, 44, 45, 46, 47, 48, 49, 50]
    rsi = ti.calculate_rsi(data, period=14)
    assert isinstance(rsi, float)
    assert 0 <= rsi <= 100

def test_calculate_rsi_insufficient_data():
    ti = TechnicalIndicators()
    data = [44, 45, 46]
    with pytest.raises(ValueError):
        ti.calculate_rsi(data, period=14)

def test_calculate_macd():
    ti = TechnicalIndicators()
    data = [i for i in range(1, 31)]  # Sample data
    macd = ti.calculate_macd(data, short_period=12, long_period=26, signal_period=9)
    assert 'macd_line' in macd
    assert 'signal_line' in macd
    assert 'histogram' in macd
    assert len(macd['macd_line']) == len(macd['signal_line']) == len(macd['histogram'])

def test_calculate_bollinger_bands():
    ti = TechnicalIndicators()
    data = [i for i in range(1, 21)]  # Sample data
    bands = ti.calculate_bollinger_bands(data, period=20, std_dev=2)
    assert 'upper' in bands
    assert 'middle' in bands
    assert 'lower' in bands

def test_calculate_bollinger_bands_insufficient_data():
    ti = TechnicalIndicators()
    data = [i for i in range(1, 10)]
    with pytest.raises(ValueError):
        ti.calculate_bollinger_bands(data, period=20, std_dev=2)