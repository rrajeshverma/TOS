from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from backtesting.trade_statistics import TradeStatistics
from domain.trade import Trade
from shared.enums import TradeStatus


def make_trade(pnl: Decimal) -> Trade:
    return Trade(
        trade_id="T1",
        risk=Mock(),
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target=Decimal("120"),
        quantity=1,
        entry_time=datetime(2026, 1, 1, 9, 15),
        status=TradeStatus.CLOSED,
        pnl=pnl,
    )


def test_total_trades():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
            make_trade(Decimal("0")),
        ]
    )

    assert statistics.total_trades == 3


def test_winning_trades():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-25")),
            make_trade(Decimal("0")),
        ]
    )

    assert statistics.winning_trades == 2


def test_losing_trades():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
            make_trade(Decimal("-25")),
            make_trade(Decimal("0")),
        ]
    )

    assert statistics.losing_trades == 2


def test_breakeven_trades():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
            make_trade(Decimal("0")),
            make_trade(Decimal("0")),
        ]
    )

    assert statistics.breakeven_trades == 2


def test_win_rate_includes_breakeven_trades():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
            make_trade(Decimal("0")),
            make_trade(Decimal("0")),
        ]
    )

    assert statistics.win_rate == 25.0


def test_empty_statistics():
    statistics = TradeStatistics([])

    assert statistics.total_trades == 0
    assert statistics.winning_trades == 0
    assert statistics.losing_trades == 0
    assert statistics.breakeven_trades == 0
    assert statistics.win_rate == 0.0
