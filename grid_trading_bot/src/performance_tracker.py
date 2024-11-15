# src/performance_tracker.py

import logging

class PerformanceTracker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.total_trades = 0
        self.total_profit = 0.0
        self.winning_trades = 0
        self.losing_trades = 0
        self.max_drawdown = 0.0
        self.peak_profit = 0.0

    def record_trade(self, profit: float):
        """
        Record the outcome of a trade.
        """
        self.total_trades += 1
        self.total_profit += profit
        if profit > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1

        # Update peak profit and drawdown
        if self.total_profit > self.peak_profit:
            self.peak_profit = self.total_profit
        drawdown = self.peak_profit - self.total_profit
        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown

        self.log_metrics()

    def get_metrics(self) -> dict:
        """
        Retrieve performance metrics.
        """
        win_rate = (self.winning_trades / self.total_trades) * 100 if self.total_trades > 0 else 0
        return {
            'total_trades': self.total_trades,
            'total_profit': self.total_profit,
            'win_rate': win_rate,
            'max_drawdown': self.max_drawdown
        }

    def log_metrics(self):
        """
        Log the current performance metrics.
        """
        metrics = self.get_metrics()
        self.logger.info(
            f"Total Trades: {metrics['total_trades']}, "
            f"Profit: {metrics['total_profit']:.2f}, "
            f"Win Rate: {metrics['win_rate']:.2f}%, "
            f"Max Drawdown: {metrics['max_drawdown']:.2f}"
        )