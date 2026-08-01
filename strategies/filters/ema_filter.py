"""
EMA filter.
"""

from __future__ import annotations


class EMAFilter:
    """
    Validates EMA breakout conditions.
    """

    def buy_allowed(
        self,
        close: float,
        ema_high: float,
    ) -> bool:
        return close > ema_high

    def sell_allowed(
        self,
        close: float,
        ema_low: float,
    ) -> bool:
        return close < ema_low
