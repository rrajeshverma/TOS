"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Ledger
Version     : 1.1.0
Author      : Rajesh Varma
Description : Stores completed trades for reporting.
=========================================================
"""

from __future__ import annotations

from domain.trade import Trade


class TradeLedger:
    """
    Stores completed trades in chronological order.
    """

    def __init__(self) -> None:
        self._trades: list[Trade] = []

    def add(
        self,
        trade: Trade,
    ) -> None:
        """
        Add a completed trade.
        """
        self._trades.append(trade)

    @property
    def trades(self) -> list[Trade]:
        """
        Return all completed trades.
        """
        return list(self._trades)

    @property
    def total_trades(self) -> int:
        """
        Number of completed trades.
        """
        return len(self._trades)
