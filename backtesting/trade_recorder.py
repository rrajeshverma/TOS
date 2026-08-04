"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Recorder
Version     : 1.1.0
Author      : Rajesh Varma
Description : Records completed trades during backtesting.
=========================================================
"""

from __future__ import annotations

from domain.trade import Trade


class TradeRecorder:
    """
    Stores completed trades generated during backtesting.

    This class is intentionally lightweight. Statistics and
    reporting are handled by dedicated components.
    """

    def __init__(self) -> None:
        self._trades: list[Trade] = []

    def record(
        self,
        trade: Trade,
    ) -> None:
        """
        Record a completed trade.
        """
        self._trades.append(trade)

    @property
    def trades(self) -> list[Trade]:
        """
        Return all recorded trades.
        """
        return list(self._trades)

    @property
    def total_trades(self) -> int:
        """
        Return total number of completed trades.
        """
        return len(self._trades)

    def clear(self) -> None:
        """
        Remove all recorded trades.
        """
        self._trades.clear()
