"""
Historical Backtest Engine.

Coordinates historical replay using TradingRuntime.
"""

from __future__ import annotations

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

    def run(self) -> int:
        processed = self._runner.run()

        statistics = TradeStatistics(
            self.context.trade_ledger.trades,
        )

        report = PerformanceReport(
            statistics,
        )

        report.print()

        return processed
