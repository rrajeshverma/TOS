from decimal import Decimal
from unittest.mock import Mock

from backtesting.performance_report import PerformanceReport
from backtesting.trade_statistics import TradeStatistics


def test_report_includes_breakeven_trades(capsys):
    statistics = TradeStatistics(
        [
            Mock(pnl=Decimal("100")),
            Mock(pnl=Decimal("-50")),
            Mock(pnl=Decimal("0")),
        ]
    )

    PerformanceReport(statistics).print()

    output = capsys.readouterr().out

    assert "Breakeven       : 1" in output
