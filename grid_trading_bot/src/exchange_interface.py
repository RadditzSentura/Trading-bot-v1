# src/exchange_interface.py

import ccxt
import base64
import logging

class ExchangeInterface:
    def __init__(self, exchange_id: str, api_key: str, api_secret: str, test_mode: bool = True):
        self.logger = logging.getLogger(__name__)
        self.exchange_id = exchange_id.lower()
        self.api_key = api_key
        self.api_secret = api_secret
        self.test_mode = test_mode

        # Validate API secret
        if not self.is_base64(api_secret):
            self.logger.error("API secret is not valid base64")
            raise ValueError("Invalid API credentials format")

        # Initialize exchange
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future' if 'future' in exchange_class().urls else 'spot',
                },
            })
            if self.test_mode:
                if 'sandbox' in self.exchange.urls:
                    self.exchange.set_sandbox_mode(True)
                    self.logger.info(f"Sandbox mode enabled for {self.exchange_id}.")
                else:
                    self.logger.error(f"Failed to initialize exchange: {self.exchange_id} does not have a sandbox URL")
                    raise ValueError(f"{self.exchange_id} does not have a sandbox URL")
            self.logger.info(f"Exchange {self.exchange_id} initialized successfully.")
        except AttributeError:
            self.logger.error(f"Exchange {self.exchange_id} not supported by ccxt.")
            raise ValueError(f"Exchange {self.exchange_id} not supported by ccxt.")
        except Exception as e:
            self.logger.error(f"Failed to initialize exchange: {e}")
            raise

    def is_base64(self, s: str) -> bool:
        try:
            return base64.b64encode(base64.b64decode(s)) == s.encode()
        except Exception:
            return False

    def get_current_price(self, symbol: str) -> float:
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            self.logger.debug(f"Fetched current price for {symbol}: {ticker['last']}")
            return ticker['last']
        except Exception as e:
            self.logger.error(f"Error fetching current price for {symbol}: {e}")
            raise

    def create_limit_order(self, symbol: str, side: str, amount: float, price: float) -> dict:
        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            self.logger.info(f"Placed {side} limit order for {amount} {symbol} at {price}")
            return order
        except ccxt.NetworkError as e:
            self.logger.error(f"Network error while creating order: {e}")
            raise
        except ccxt.ExchangeError as e:
            self.logger.error(f"Exchange error while creating order: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while creating order: {e}")
            raise

    def cancel_order(self, order_id: str) -> bool:
        try:
            result = self.exchange.cancel_order(order_id)
            self.logger.info(f"Cancelled order {order_id}")
            return result
        except ccxt.NetworkError as e:
            self.logger.error(f"Network error while cancelling order {order_id}: {e}")
            raise
        except ccxt.ExchangeError as e:
            self.logger.error(f"Exchange error while cancelling order {order_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while cancelling order {order_id}: {e}")
            raise

    def get_active_orders(self, symbol: str) -> list:
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            self.logger.debug(f"Fetched {len(orders)} active orders for {symbol}")
            return orders
        except ccxt.NetworkError as e:
            self.logger.error(f"Network error while fetching active orders for {symbol}: {e}")
            raise
        except ccxt.ExchangeError as e:
            self.logger.error(f"Exchange error while fetching active orders for {symbol}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while fetching active orders for {symbol}: {e}")
            raise