"""
In-memory trade journal for historical backtesting.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from domain.trade import Trade
from shared.enums import TradeStatus


class BacktestTradeJournal:
    """
    Provides daily trade statistics from the current backtest session.

    No persistent files are used.
    """

    def __init__(self) -> None:
        self._trades: list[Trade] = []

    def record(self, trade: Trade) -> None:
        """
        Record a completed trade.
        """

        if trade.status != TradeStatus.CLOSED:
            return

        self._trades.append(trade)

    def count_today(
        self,
        trade_date: date | None = None,
    ) -> int:
        """
        Return the number of completed trades for the given date.
        """

        if trade_date is None:
            trade_date = date.today()

        return sum(
            1
            for trade in self._trades
            if trade.exit_time is not None and trade.exit_time.date() == trade_date
        )

    def daily_pnl(
        self,
        trade_date: date | None = None,
    ) -> Decimal:
        """
        Return realized P&L for the given date.
        """

        if trade_date is None:
            trade_date = date.today()

        return sum(
            (
                trade.pnl
                for trade in self._trades
                if trade.exit_time is not None and trade.exit_time.date() == trade_date
            ),
            Decimal("0"),
        )
