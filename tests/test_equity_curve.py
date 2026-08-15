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


def test_equity_curve():
    curve = EquityCurve(
        [
            make_trade(Decimal("100")),
            make_trade(Decimal("-50")),
            make_trade(Decimal("200")),
        ]
    )

    assert curve.values() == [
        Decimal("100"),
        Decimal("50"),
        Decimal("250"),
    ]
