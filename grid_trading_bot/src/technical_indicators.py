# src/technical_indicators.py

import logging
from typing import List, Dict

class TechnicalIndicators:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_rsi(self, data: List[float], period: int = 14) -> float:
        """
        Calculate the Relative Strength Index (RSI).
        """
        try:
            if not data or len(data) < period + 1:
                self.logger.error(f"Invalid data for RSI calculation: {data}")
                raise ValueError("Insufficient data for RSI calculation")

            gains = []
            losses = []
            for i in range(1, len(data)):
                delta = data[i] - data[i-1]
                if delta > 0:
                    gains.append(delta)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(-delta)

            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period

            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period

            if avg_loss == 0:
                return 100.0
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {e}")
            raise

    def calculate_macd(self, data: List[float], short_period: int = 12, long_period: int = 26, signal_period: int = 9) -> Dict:
        """
        Calculate the Moving Average Convergence Divergence (MACD).
        """
        try:
            short_ema = self.calculate_ema(data, short_period)
            long_ema = self.calculate_ema(data, long_period)
            macd_line = [s - l for s, l in zip(short_ema, long_ema)]
            signal_line = self.calculate_ema(macd_line, signal_period)
            histogram = [m - s for m, s in zip(macd_line, signal_line)]
            return {'macd_line': macd_line, 'signal_line': signal_line, 'histogram': histogram}
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {e}")
            raise

    def calculate_ema(self, data: List[float], period: int) -> List[float]:
        """
        Calculate the Exponential Moving Average (EMA).
        """
        try:
            if len(data) < period:
                self.logger.error("Insufficient data for EMA calculation")
                raise ValueError("Insufficient data for EMA calculation")

            alpha = 2 / (period + 1)
            ema = [sum(data[:period]) / period]  # Simple Moving Average for the first EMA
            for price in data[period:]:
                ema.append(alpha * price + (1 - alpha) * ema[-1])
            return ema
        except Exception as e:
            self.logger.error(f"Error calculating EMA: {e}")
            raise

    def calculate_bollinger_bands(self, data: List[float], period: int = 20, std_dev: int = 2) -> Dict:
        """
        Calculate Bollinger Bands.
        """
        try:
            if len(data) < period:
                self.logger.error("Insufficient data for Bollinger Bands calculation")
                raise ValueError("Insufficient data for Bollinger Bands calculation")

            sma = sum(data[-period:]) / period  # Simple Moving Average
            variance = sum([(price - sma) ** 2 for price in data[-period:]]) / period
            std_deviation = variance ** 0.5
            upper_band = sma + (std_dev * std_deviation)
            lower_band = sma - (std_dev * std_deviation)
            return {'upper': upper_band, 'middle': sma, 'lower': lower_band}
        except Exception as e:
            self.logger.error(f"Error calculating Bollinger Bands: {e}")
            raise