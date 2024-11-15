# src/strategies/default_strategy.py

from .base_strategy import BaseStrategy
from typing import List, Dict
import logging

class DefaultStrategy(BaseStrategy):
    def __init__(self, parameters: Dict):
        super().__init__(parameters)
        self.volatility_period = self.parameters.get('volatility_period', 14)
        self.rsi_threshold = self.parameters.get('rsi_threshold', 70)
        self.macd_fast_period = self.parameters.get('macd_fast_period', 12)
        self.macd_slow_period = self.parameters.get('macd_slow_period', 26)
        self.macd_signal_period = self.parameters.get('macd_signal_period', 9)

    def decide(self, current_price: float, grids: List[float], quantities: List[float], data: Dict) -> List[Dict]:
        """
        Default strategy based on RSI and MACD indicators.
        """
        decisions = []
        rsi = data.get('rsi')
        macd = data.get('macd')

        # Example Decision Logic:
        # Buy if RSI is below a certain threshold
        # Sell if MACD histogram is positive

        if rsi is not None and rsi < self.rsi_threshold:
            # Find the grid level to buy
            for price, qty in zip(grids, quantities):
                if current_price <= price:
                    decision = {
                        'side': 'buy',
                        'amount': qty,
                        'price': price
                    }
                    decisions.append(decision)
                    self.logger.debug(f"RSI condition met. Decided to buy at {price} for {qty}")
                    break  # Buy at the first grid level that meets the condition

        if macd is not None:
            histogram = macd.get('histogram', [])
            if histogram and histogram[-1] > 0:
                # Find the grid level to sell
                for price, qty in zip(grids, quantities):
                    sell_price = price * 1.01  # Example: sell 1% above grid price
                    decision = {
                        'side': 'sell',
                        'amount': qty,
                        'price': round(sell_price, 2),
                        'profit': sell_price - price
                    }
                    decisions.append(decision)
                    self.logger.debug(f"MACD condition met. Decided to sell at {sell_price} for profit {sell_price - price}")
                    break  # Sell at the first grid level that meets the condition

        return decisions