"""
VWAP filter.
"""

from __future__ import annotations


class VWAPFilter:
    """
    Validates VWAP conditions.
    """

    def buy_allowed(
        self,
        close: float,
        vwap: float,
    ) -> bool:
        return close > vwap

    def sell_allowed(
        self,
        close: float,
        vwap: float,
    ) -> bool:
        return close < vwap
