"""
RSI filter.
"""

from __future__ import annotations


class RSIFilter:
    """
    Validates RSI thresholds.
    """

    BUY_LEVEL = 55
    SELL_LEVEL = 45

    def buy_allowed(
        self,
        rsi: float,
    ) -> bool:
        return rsi > self.BUY_LEVEL

    def sell_allowed(
        self,
        rsi: float,
    ) -> bool:
        return rsi < self.SELL_LEVEL

    def neutral(
        self,
        rsi: float,
    ) -> bool:
        return self.SELL_LEVEL <= rsi <= self.BUY_LEVEL
