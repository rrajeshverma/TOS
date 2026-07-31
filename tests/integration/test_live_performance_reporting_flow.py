"""
Integration test:
Trade Data -> Performance Service -> Performance Metrics
"""

from dataclasses import dataclass
from decimal import Decimal

from reporting.models.performance_summary import PerformanceSummary
from reporting.services.performance_service import PerformanceService
from reporting.reports.trade_statistics import TradeStatistics


@dataclass
class FakeTrade:
    pnl: Decimal


def create_trades():
    return [
        FakeTrade(pnl=Decimal("1000")),
        FakeTrade(pnl=Decimal("-200")),
        FakeTrade(pnl=Decimal("500")),
    ]


def test_trade_statistics_calculation():
    trades = create_trades()

    statistics = TradeStatistics()

    assert statistics.total_trades(trades) == 3
    assert statistics.winning_trades(trades) == 2
    assert statistics.losing_trades(trades) == 1


def test_trade_statistics_profit_metrics():
    trades = create_trades()

    statistics = TradeStatistics()

    assert statistics.gross_profit(trades) == Decimal("1500")
    assert statistics.gross_loss(trades) == Decimal("200")


def test_performance_service_generates_metrics():
    trades = create_trades()

    service = PerformanceService()

    result = service.calculate(trades)

    assert result.total_trades == 3
    assert result.winning_trades == 2
    assert result.losing_trades == 1
    assert result.net_profit == Decimal("1300")


def test_performance_summary_structure():
    summary = PerformanceSummary()

    assert summary.trade_metrics is None
    assert summary.portfolio_metrics == {}
