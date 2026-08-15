"""
Historical Backtest Engine.

Coordinates historical replay using TradingRuntime.
"""

from __future__ import annotations

from decimal import Decimal

from backtesting.equity_curve import EquityCurve
from backtesting.performance_report import PerformanceReport
from backtesting.trade_statistics import TradeStatistics


class HistoricalBacktestEngine:
    """
    Coordinates the complete historical replay backtest.
    """

    def __init__(
        self,
        runtime,
        replay_runner,
        initial_capital: Decimal = Decimal("100000"),
    ) -> None:
        self._runtime = runtime
        self._runner = replay_runner
        self.context = replay_runner.context
        self.equity_curve = EquityCurve([])
        self._initial_capital = initial_capital
        self.statistics = TradeStatistics(
            [],
            initial_capital=self._initial_capital,
        )

    def run(self) -> int:
        processed = self._runner.run()

        trades = self.context.trade_ledger.trades
        self.equity_curve = EquityCurve(trades)

        self.statistics = TradeStatistics(
            trades,
            initial_capital=self._initial_capital,
        )

        report = PerformanceReport(
            self.statistics,
        )

        report.print()

        return processed
