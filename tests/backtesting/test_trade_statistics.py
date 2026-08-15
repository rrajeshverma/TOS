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


def test_average_win():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-25")),
        ]
    )

    assert statistics.average_win == Decimal("75")


def test_average_loss():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
            make_trade(Decimal("-25")),
        ]
    )

    assert statistics.average_loss == Decimal("-37.5")


def test_profit_factor():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-25")),
            make_trade(Decimal("-25")),
        ]
    )

    assert statistics.profit_factor == Decimal("3")


def test_profit_factor_with_no_losses():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
        ]
    )

    assert statistics.profit_factor == Decimal("0")


def test_expectancy():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-25")),
            make_trade(Decimal("-25")),
        ]
    )

    assert statistics.expectancy == Decimal("25")


def test_expectancy_empty_statistics():
    statistics = TradeStatistics([])

    assert statistics.expectancy == Decimal("0")


def test_maximum_drawdown():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-80")),
            make_trade(Decimal("-100")),
            make_trade(Decimal("40")),
        ]
    )

    assert statistics.maximum_drawdown == Decimal("180")


def test_maximum_drawdown_empty_statistics():
    statistics = TradeStatistics([])

    assert statistics.maximum_drawdown == Decimal("0")


def test_maximum_drawdown_with_only_profit():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("25")),
        ]
    )

    assert statistics.maximum_drawdown == Decimal("0")


def test_maximum_drawdown_percentage():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-80")),
            make_trade(Decimal("-100")),
            make_trade(Decimal("40")),
        ],
        initial_capital=Decimal("1000"),
    )

    assert statistics.maximum_drawdown_percentage == Decimal("18")


def test_maximum_drawdown_percentage_empty_statistics():
    statistics = TradeStatistics(
        [],
        initial_capital=Decimal("1000"),
    )

    assert statistics.maximum_drawdown_percentage == Decimal("0")


def test_maximum_drawdown_percentage_with_zero_capital():
    statistics = TradeStatistics(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
        ],
        initial_capital=Decimal("0"),
    )

    assert statistics.maximum_drawdown_percentage == Decimal("0")
