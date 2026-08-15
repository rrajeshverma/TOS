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


def test_report_includes_performance_metrics(capsys):
    statistics = TradeStatistics(
        [
            Mock(pnl=Decimal("100")),
            Mock(pnl=Decimal("50")),
            Mock(pnl=Decimal("-25")),
            Mock(pnl=Decimal("-25")),
        ]
    )

    PerformanceReport(statistics).print()

    output = capsys.readouterr().out

    assert "Average Win     : 75" in output
    assert "Average Loss    : -25" in output
    assert "Profit Factor   : 3" in output
    assert "Expectancy      : 25" in output


def test_report_includes_maximum_drawdown(capsys):
    statistics = TradeStatistics(
        [
            Mock(pnl=Decimal("100")),
            Mock(pnl=Decimal("50")),
            Mock(pnl=Decimal("-80")),
            Mock(pnl=Decimal("-100")),
            Mock(pnl=Decimal("40")),
        ]
    )

    PerformanceReport(statistics).print()

    output = capsys.readouterr().out

    assert "Maximum Drawdown: 180" in output


def test_report_includes_maximum_drawdown_percentage(capsys):
    statistics = TradeStatistics(
        [
            Mock(pnl=Decimal("100")),
            Mock(pnl=Decimal("50")),
            Mock(pnl=Decimal("-80")),
            Mock(pnl=Decimal("-100")),
            Mock(pnl=Decimal("40")),
        ],
        initial_capital=Decimal("1000"),
    )

    PerformanceReport(statistics).print()

    output = capsys.readouterr().out

    assert "Maximum Drawdown %: 18" in output
