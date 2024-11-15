# src/advanced_grid_trading_bot.py

import logging
import time
import signal
import sys
from typing import List, Dict

from exchange_interface import ExchangeInterface
from grid_calculator import GridCalculator
from order_manager import OrderManager
from technical_indicators import TechnicalIndicators
from performance_tracker import PerformanceTracker
from config_loader import ConfigLoader
from strategies.base_strategy import BaseStrategy
from strategies.default_strategy import DefaultStrategy

class AdvancedGridTradingBot:
    def __init__(self, config: dict):
        self.logger = logging.getLogger(__name__)
        self.running = True

        # Load configurations
        exchange_cfg = config['exchange']
        trading_cfg = config['trading']
        performance_cfg = config['performance']

        # Initialize components
        self.exchange_interface = ExchangeInterface(
            exchange_id=exchange_cfg['id'],
            api_key=exchange_cfg['api_key'],
            api_secret=exchange_cfg['api_secret'],
            test_mode=exchange_cfg.get('test_mode', True)
        )

        self.grid_calculator = GridCalculator(
            lower_price=trading_cfg['lower_price'],
            upper_price=trading_cfg['upper_price'],
            grid_quantity=trading_cfg['grid_quantity'],
            total_investment=trading_cfg['total_investment']
        )

        self.order_manager = OrderManager(exchange=self.exchange_interface)
        self.tech_indicators = TechnicalIndicators()
        self.performance_tracker = PerformanceTracker()

        # Trading parameters
        self.symbol = trading_cfg['symbol']
        self.stop_loss = trading_cfg.get('stop_loss')
        self.trailing_stop_enabled = trading_cfg.get('trailing_stop', {}).get('enabled', False)
        self.trailing_stop_percentage = trading_cfg.get('trailing_stop', {}).get('percentage', 0.05)
        self.dynamic_grids = trading_cfg.get('dynamic_grids', False)
        self.volatility_threshold = trading_cfg.get('strategy', {}).get('parameters', {}).get('volatility_period', 14)
        self.rsi_threshold = trading_cfg.get('strategy', {}).get('parameters', {}).get('rsi_threshold', 70)
        self.macd_fast_period = trading_cfg.get('strategy', {}).get('parameters', {}).get('macd_fast_period', 12)
        self.macd_slow_period = trading_cfg.get('strategy', {}).get('parameters', {}).get('macd_slow_period', 26)
        self.macd_signal_period = trading_cfg.get('strategy', {}).get('parameters', {}).get('macd_signal_period', 9)
        self.price_precision = 2  # Decimal places for price

        # Trailing stop variables
        self.trailing_stop_price = None

        # Initialize strategy
        strategy_type = trading_cfg.get('strategy', {}).get('type', 'default')
        strategy_parameters = trading_cfg.get('strategy', {}).get('parameters', {})
        self.strategy = self.initialize_strategy(strategy_type, strategy_parameters)

        # Setup initial grids
        self.place_grid_orders()

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        self.logger.info("AdvancedGridTradingBot initialized successfully.")

    def initialize_strategy(self, strategy_type: str, parameters: Dict) -> BaseStrategy:
        """
        Initialize the trading strategy based on configuration.
        """
        try:
            if strategy_type == "default":
                strategy = DefaultStrategy(parameters)
            else:
                self.logger.error(f"Strategy type '{strategy_type}' is not recognized.")
                raise ValueError(f"Strategy type '{strategy_type}' is not recognized.")
            self.logger.info(f"Initialized strategy: {strategy_type}")
            return strategy
        except Exception as e:
            self.logger.error(f"Error initializing strategy '{strategy_type}': {e}")
            raise

    def place_grid_orders(self, prices: List[float] = None, quantities: List[float] = None):
        if prices is None or quantities is None:
            grid = self.grid_calculator.calculate_static_grids()
            prices = grid['prices']
            quantities = grid['quantities']
            self.logger.info("Placing static grid orders.")

        for price, qty in zip(prices, quantities):
            # Place buy and sell orders
            try:
                buy_order = self.order_manager.place_limit_order(
                    symbol=self.symbol,
                    side='buy',
                    amount=qty,
                    price=price
                )
                sell_price = round(price * 1.01, self.price_precision)  # Example: sell 1% above buy price
                sell_order = self.order_manager.place_limit_order(
                    symbol=self.symbol,
                    side='sell',
                    amount=qty,
                    price=sell_price
                )
                self.logger.debug(f"Placed buy order at {price} and sell order at {sell_price}")
            except Exception as e:
                self.logger.error(f"Failed to place grid orders at price {price}: {e}")

    def adjust_grids(self, current_price: float, volatility: float):
        if self.dynamic_grids and volatility > self.volatility_threshold:
            self.logger.info(f"Adjusting grids based on volatility: {volatility}")
            try:
                new_grids = self.grid_calculator.calculate_dynamic_grids(
                    current_price=current_price,
                    volatility=volatility,
                    price_precision=self.price_precision
                )
                self.order_manager.cancel_all_orders(self.symbol)
                self.place_grid_orders(prices=new_grids['prices'], quantities=new_grids['quantities'])
                self.logger.info("Grid adjustment completed.")
            except Exception as e:
                self.logger.error(f"Error adjusting grids: {e}")

    def check_stop_loss(self, current_price: float):
        if self.stop_loss and current_price < self.stop_loss:
            self.logger.info(f"Stop-loss triggered at {current_price}. Shutting down bot.")
            self._shutdown()

    def apply_trailing_stop(self, current_price: float):
        if self.trailing_stop_enabled:
            if self.trailing_stop_price is None or current_price > (self.trailing_stop_price / (1 - self.trailing_stop_percentage)):
                self.trailing_stop_price = current_price * (1 - self.trailing_stop_percentage)
                self.logger.info(f"Trailing stop updated to {self.trailing_stop_price}")

    def monitor_performance(self):
        self.performance_tracker.log_metrics()

    def get_status(self) -> dict:
        try:
            current_price = self.exchange_interface.get_current_price(self.symbol)
            active_orders = self.order_manager.get_active_orders(self.symbol)
            metrics = self.performance_tracker.get_metrics()
            status = {
                'current_price': current_price,
                'active_orders': active_orders,
                'performance_metrics': metrics
            }
            self.logger.info(f"Status Update: {status}")
            return status
        except Exception as e:
            self.logger.error(f"Error retrieving status: {e}")
            return {}

    def run(self):
        self.logger.info("Bot is running.")
        while self.running:
            try:
                current_price = self.exchange_interface.get_current_price(self.symbol)
                # Fetch historical price data for indicators
                price_history = self.fetch_price_history(period=self.volatility_threshold)

                # Calculate technical indicators
                rsi = self.tech_indicators.calculate_rsi(price_history, period=self.volatility_threshold)
                macd = self.tech_indicators.calculate_macd(
                    price_history,
                    short_period=self.macd_fast_period,
                    long_period=self.macd_slow_period,
                    signal_period=self.macd_signal_period
                )

                # Prepare data for strategy
                strategy_data = {
                    'rsi': rsi,
                    'macd': macd
                }

                # Apply trailing stop
                if self.trailing_stop_enabled:
                    self.apply_trailing_stop(current_price)

                # Check stop-loss
                self.check_stop_loss(current_price)

                # Decide on trading actions
                decisions = self.strategy.decide(current_price, self.grid_calculator.calculate_static_grids()['prices'], self.grid_calculator.calculate_static_grids()['quantities'], strategy_data)
                for decision in decisions:
                    side = decision['side']
                    amount = decision['amount']
                    price = decision['price']
                    profit = decision.get('profit', 0.0)
                    try:
                        if side.lower() == 'buy':
                            # Place buy order
                            self.order_manager.place_limit_order(self.symbol, side, amount, price)
                            self.performance_tracker.record_trade(-amount * price)  # Buying reduces profit
                            self.logger.debug(f"Executed buy at {price} for amount {amount}")
                        elif side.lower() == 'sell':
                            # Place sell order
                            self.order_manager.place_limit_order(self.symbol, side, amount, price)
                            self.performance_tracker.record_trade(profit)
                            self.logger.debug(f"Executed sell at {price} with profit {profit}")
                    except Exception as e:
                        self.logger.error(f"Error executing decision: {e}")

                # Adjust grids dynamically based on volatility
                self.adjust_grids(current_price, self.calculate_volatility(rsi))

                # Monitor performance at intervals
                self.monitor_performance()

                # Sleep for a defined interval (e.g., 60 seconds)
                time.sleep(performance_cfg.get('log_interval', 60))

            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                time.sleep(60)  # Wait before retrying

    def calculate_volatility(self, rsi: float) -> float:
        """
        Calculate volatility based on RSI.
        """
        # Example volatility calculation based on RSI
        if rsi > self.rsi_threshold:
            return 10.0  # High volatility
        else:
            return 5.0   # Low volatility

    def fetch_price_history(self, period: int) -> List[float]:
        """
        Fetch historical price data required for indicator calculations.
        """
        try:
            # Example: Fetch the last 'period' number of closing prices
            historical_data = self.exchange_interface.exchange.fetch_ohlcv(
                self.symbol,
                timeframe='1h',
                limit=period
            )
            prices = [entry[4] for entry in historical_data]  # Closing prices
            return prices
        except Exception as e:
            self.logger.error(f"Error fetching price history: {e}")
            raise

    def handle_shutdown(self, signum, frame):
        self.logger.info(f"Received shutdown signal: {signum}")
        self._shutdown()

    def _shutdown(self):
        if not self.running:
            return
        self.running = False
        self.logger.info("Shutting down bot...")
        try:
            self.order_manager.cancel_all_orders(self.symbol)
            self.logger.info("All active orders have been cancelled.")
        except Exception as e:
            self.logger.error(f"Error cancelling orders during shutdown: {e}")
        self.performance_tracker.log_metrics()
        self.logger.info("Bot shutdown complete.")
        sys.exit(0)