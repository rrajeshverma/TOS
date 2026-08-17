"""
Daily trade-entry execution guard.
"""

from __future__ import annotations

from datetime import date

from config.risk import MAX_TRADES_PER_DAY


class TradeLimitGuard:
    """
    Blocks new entries once the daily entry limit is reached.
    """

    def __init__(
        self,
        max_trades: int = MAX_TRADES_PER_DAY,
    ) -> None:
        if max_trades <= 0:
            raise ValueError("max_trades must be greater than zero")

        self._max_trades = max_trades
        self._trade_date = date.today()
        self._submitted = 0

    def can_execute(self) -> bool:
        self._reset_if_new_day()
        return self._submitted < self._max_trades

    def record_execution(self) -> None:
        self._reset_if_new_day()
        self._submitted += 1

    @property
    def submitted(self) -> int:
        self._reset_if_new_day()
        return self._submitted

    def _reset_if_new_day(self) -> None:
        today = date.today()

        if today != self._trade_date:
            self._trade_date = today
            self._submitted = 0
