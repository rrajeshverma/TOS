from decimal import Decimal

from portfolio.position_aggregator import PositionAggregator


class FakePosition:
    def __init__(
        self,
        quantity,
        average_price,
        last_price,
    ):
        self.quantity = quantity
        self.average_price = Decimal(str(average_price))
        self.last_traded_price = Decimal(str(last_price))


def test_build_snapshot():
    positions = [
        FakePosition(
            65,
            25000,
            25100,
        )
    ]

    snapshot = PositionAggregator().build_snapshot(
        positions,
        cash=100000,
        realized_pnl=Decimal(1000),
    )

    assert snapshot.cash == 100000
    assert snapshot.open_positions == 1
    assert snapshot.unrealized_pnl == Decimal(6500)
    assert snapshot.total_pnl() == Decimal(7500)
    assert snapshot.equity == Decimal(107500)
