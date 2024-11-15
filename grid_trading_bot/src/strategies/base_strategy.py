# src/strategies/base_strategy.py

from abc import ABC, abstractmethod
from typing import List, Dict
import logging

class BaseStrategy(ABC):
    def __init__(self, parameters: Dict):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.parameters = parameters

    @abstractmethod
    def decide(self, current_price: float, grids: List[float], quantities: List[float], data: Dict) -> List[Dict]:
        """
        Decide on trading actions based on current market data.
        :return: List of decisions with 'side', 'amount', 'price', and optionally 'profit'.
        """
        pass