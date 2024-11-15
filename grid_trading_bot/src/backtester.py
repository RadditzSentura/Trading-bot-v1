# src/backtester.py

import pandas as pd
import logging
from typing import List, Dict

class Backtester:
    def __init__(self, grid_calculator, order_manager, tech_indicators, performance_tracker, strategy):
        self.logger = logging.getLogger(__name__)
        self.grid_calculator = grid_calculator
        self.order_manager = order_manager
        self.tech_indicators = tech_indicators
        self.performance_tracker = performance_tracker
        self.strategy = strategy

    def run_backtest(self, historical_data: pd.DataFrame):
        """
        Simulate trading based on historical data.
        :param historical_data: DataFrame with 'timestamp', 'price', and other relevant columns.
        """
        self.logger.info("Starting backtest.")
        # Initialize grids
        grid = self.grid_calculator.calculate_static_grids()
        grids = grid['prices']
        quantities = grid['quantities']

        for index, row in historical_data.iterrows():
            current_price = row['price']
            timestamp = row['timestamp']
            self.logger.debug(f"Backtest Timestamp: {timestamp}, Current Price: {current_price}")

            # Apply strategy to decide whether to place orders
            decisions = self.strategy.decide(current_price, grids, quantities, row)
            for decision in decisions:
                side = decision['side']
                amount = decision['amount']
                price = decision['price']
                profit = decision.get('profit', 0.0)
                try:
                    if side.lower() == 'buy':
                        # Simulate buy
                        self.performance_tracker.record_trade(-amount * price)  # Buying reduces profit
                        self.logger.debug(f"Simulated buy at {price} for amount {amount}")
                    elif side.lower() == 'sell':
                        # Simulate sell
                        self.performance_tracker.record_trade(profit)
                        self.logger.debug(f"Simulated sell at {price} with profit {profit}")
                except Exception as e:
                    self.logger.error(f"Error during backtest decision execution: {e}")

        self.logger.info("Backtest completed.")
        metrics = self.performance_tracker.get_metrics()
        self.logger.info(f"Backtest Metrics: {metrics}")
        return metrics