"""
Confirmation candle filter.
"""

from __future__ import annotations


class ConfirmationFilter:
    """
    Confirms breakout using
    the next candle.
    """

    def buy_allowed(
        self,
        signal_high: float,
        current_high: float,
    ) -> bool:
        return current_high > signal_high

    def sell_allowed(
        self,
        signal_low: float,
        current_low: float,
    ) -> bool:
        return current_low < signal_low
