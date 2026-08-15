"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Statistics
Version     : 1.1.0
Author      : Rajesh Varma
Description : Calculates trade performance statistics.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal

from backtesting.drawdown import Drawdown
from backtesting.equity_curve import EquityCurve
from domain.trade import Trade


class TradeStatistics:
    """
    Calculates statistics for completed trades.
    """

    def __init__(
        self,
        trades: list[Trade],
        initial_capital: Decimal = Decimal("100000"),
    ) -> None:
        self._trades = trades
        self._initial_capital = initial_capital

    @property
    def total_trades(self) -> int:
        return len(self._trades)

    @property
    def winning_trades(self) -> int:
        return sum(1 for trade in self._trades if trade.pnl > Decimal(0))

    @property
    def losing_trades(self) -> int:
        return sum(1 for trade in self._trades if trade.pnl < Decimal(0))

    @property
    def breakeven_trades(self) -> int:
        return sum(1 for trade in self._trades if trade.pnl == Decimal(0))

    @property
    def gross_profit(self) -> Decimal:
        return sum(
            (trade.pnl for trade in self._trades if trade.pnl > Decimal(0)),
            Decimal(0),
        )

    @property
    def gross_loss(self) -> Decimal:
        return sum(
            (trade.pnl for trade in self._trades if trade.pnl < Decimal(0)),
            Decimal(0),
        )

    @property
    def net_profit(self) -> Decimal:
        return self.gross_profit + self.gross_loss

    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0

        return (self.winning_trades / self.total_trades) * 100

    @property
    def average_win(self) -> Decimal:
        if self.winning_trades == 0:
            return Decimal(0)

        return self.gross_profit / self.winning_trades

    @property
    def average_loss(self) -> Decimal:
        if self.losing_trades == 0:
            return Decimal(0)

        return self.gross_loss / self.losing_trades

    @property
    def profit_factor(self) -> Decimal:
        if self.gross_loss == Decimal(0):
            return Decimal(0)

        return self.gross_profit / abs(self.gross_loss)

    @property
    def expectancy(self) -> Decimal:
        if self.total_trades == 0:
            return Decimal(0)

        return self.net_profit / self.total_trades

    @property
    def maximum_drawdown(self) -> Decimal:
        equity = EquityCurve(self._trades).values()

        return Drawdown(equity).maximum

    @property
    def maximum_drawdown_percentage(self) -> Decimal:
        equity = EquityCurve(self._trades).values()

        return Drawdown(equity).maximum_percentage(
            self._initial_capital,
        )
