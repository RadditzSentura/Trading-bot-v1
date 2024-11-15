# src/grid_calculator.py

import numpy as np
import logging

class GridCalculator:
    def __init__(self, lower_price: float, upper_price: float, grid_quantity: int, total_investment: float):
        self.logger = logging.getLogger(__name__)
        self.lower_price = lower_price
        self.upper_price = upper_price
        self.grid_quantity = grid_quantity
        self.total_investment = total_investment
        self.min_order_size = 0.001  # Example minimum order size

    def calculate_static_grids(self) -> dict:
        """
        Calculate static grid levels and quantities.
        """
        try:
            prices = np.linspace(self.lower_price, self.upper_price, self.grid_quantity + 1)
            grid_spacing = prices[1] - prices[0]
            quantity = self.total_investment / self.upper_price / self.grid_quantity
            quantities = [quantity] * len(prices)
            self.logger.debug(f"Calculated static grids: {len(prices)} levels.")
            return {'prices': prices.tolist(), 'quantities': quantities}
        except Exception as e:
            self.logger.error(f"Error calculating static grids: {e}")
            raise

    def calculate_dynamic_grids(self, current_price: float, volatility: float, price_precision: int) -> dict:
        """
        Calculate dynamic grid levels based on market volatility.
        """
        try:
            if current_price < self.lower_price or current_price > self.upper_price:
                self.logger.error(f"Error calculating grid levels: Price {current_price} is out of range")
                raise ValueError(f"Price {current_price} is out of range")

            # Adjust grid spacing based on volatility
            adjusted_grid_quantity = max(1, int(self.grid_quantity * (volatility / 100)))
            prices = np.linspace(self.lower_price, self.upper_price, adjusted_grid_quantity + 1)
            prices = [round(price, price_precision) for price in prices]
            quantity = self.total_investment / self.upper_price / adjusted_grid_quantity
            quantities = [quantity] * len(prices)
            self.logger.debug(f"Calculated dynamic grids based on volatility {volatility}: {len(prices)} levels.")
            return {'prices': prices, 'quantities': quantities}
        except Exception as e:
            self.logger.error(f"Error calculating dynamic grids: {e}")
            raise