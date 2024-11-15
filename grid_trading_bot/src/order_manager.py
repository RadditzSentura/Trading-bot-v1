# src/order_manager.py

import logging
from typing import List, Dict

class OrderManager:
    def __init__(self, exchange: 'ExchangeInterface'):
        self.logger = logging.getLogger(__name__)
        self.exchange = exchange

    def place_limit_order(self, symbol: str, side: str, amount: float, price: float) -> Dict:
        """
        Place a limit order on the exchange.
        """
        if price <= 0 or amount <= 0:
            self.logger.error(f"Error placing order: Invalid parameters - Price: {price}, Amount: {amount}")
            raise ValueError("Invalid order parameters")

        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            self.logger.info(f"Placed {side} limit order for {amount} {symbol} at {price}")
            return order
        except Exception as e:
            self.logger.error(f"Error creating order: {e}")
            raise

    def cancel_all_orders(self, symbol: str):
        """
        Cancel all active orders for a given symbol.
        """
        try:
            active_orders = self.get_active_orders(symbol)
            for order in active_orders:
                self.exchange.cancel_order(order['id'])
                self.logger.info(f"Cancelled order {order['id']}")
        except Exception as e:
            self.logger.error(f"Error cancelling all orders for {symbol}: {e}")
            raise

    def get_active_orders(self, symbol: str) -> List[Dict]:
        """
        Retrieve all active orders for a given symbol.
        """
        try:
            orders = self.exchange.get_active_orders(symbol)
            return orders
        except Exception as e:
            self.logger.error(f"Error fetching active orders for {symbol}: {e}")
            raise