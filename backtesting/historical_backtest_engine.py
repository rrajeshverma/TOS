"""
Historical Backtest Engine.

Coordinates historical replay using TradingRuntime.
"""

from __future__ import annotations

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
    ) -> None:
        self._runtime = runtime
        self._runner = replay_runner
        self.context = replay_runner.context
        self.equity_curve = EquityCurve([])

    def run(self) -> int:
        processed = self._runner.run()

        trades = self.context.trade_ledger.trades
        self.equity_curve = EquityCurve(trades)

        statistics = TradeStatistics(
            trades,
        )

        report = PerformanceReport(
            statistics,
        )

        report.print()

        return processed
