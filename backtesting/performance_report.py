"""
=========================================================
Trading Operating System (TOS)
Module      : Performance Report
Version     : 1.1.0
Author      : Rajesh Varma
Description : Prints backtesting performance summary.
=========================================================
"""

from __future__ import annotations

from backtesting.trade_statistics import TradeStatistics


class PerformanceReport:
    """
    Builds a console report for backtest performance.
    """

    def __init__(
        self,
        statistics: TradeStatistics,
    ) -> None:
        self._statistics = statistics

    def print(self) -> None:
        print()
        print("=" * 56)
        print("BACKTEST REPORT")
        print("=" * 56)

        print(f"Trades          : {self._statistics.total_trades}")
        print(f"Wins            : {self._statistics.winning_trades}")
        print(f"Losses          : {self._statistics.losing_trades}")
        print(f"Breakeven       : {self._statistics.breakeven_trades}")

        print(f"Win Rate        : {self._statistics.win_rate:.2f}%")

        print(f"Gross Profit    : {self._statistics.gross_profit}")
        print(f"Gross Loss      : {self._statistics.gross_loss}")

        print(f"Average Win     : {self._statistics.average_win}")
        print(f"Average Loss    : {self._statistics.average_loss}")
        print(f"Profit Factor   : {self._statistics.profit_factor}")
        print(f"Expectancy      : {self._statistics.expectancy}")
        print(f"Maximum Drawdown: {self._statistics.maximum_drawdown}")

        print(f"Net Profit      : {self._statistics.net_profit}")

        print("=" * 56)
