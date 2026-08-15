from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from backtesting.equity_curve import EquityCurve
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


def test_equity_curve_returns_cumulative_pnl():
    curve = EquityCurve(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("50")),
            make_trade(Decimal("-80")),
            make_trade(Decimal("-100")),
            make_trade(Decimal("40")),
        ]
    )

    assert curve.values() == [
        Decimal("100"),
        Decimal("150"),
        Decimal("70"),
        Decimal("-30"),
        Decimal("10"),
    ]


def test_equity_curve_empty_trades():
    curve = EquityCurve([])

    assert curve.values() == []


def test_equity_curve_includes_breakeven_trade():
    curve = EquityCurve(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("0")),
            make_trade(Decimal("-25")),
        ]
    )

    assert curve.values() == [
        Decimal("100"),
        Decimal("100"),
        Decimal("75"),
    ]
