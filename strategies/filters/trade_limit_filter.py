"""
Daily trade limit filter.
"""

from __future__ import annotations


class TradeLimitFilter:
    """
    Limits the number of trades
    executed during a trading day.
    """

    def __init__(
        self,
        max_trades: int = 2,
    ) -> None:
        self._max_trades = max_trades

    def allow(
        self,
        trades_today: int,
    ) -> bool:
        return trades_today < self._max_trades
