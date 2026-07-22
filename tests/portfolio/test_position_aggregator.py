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


def test_empty_positions():

    aggregator = PositionAggregator()

    assert aggregator.position_count([]) == 0


def test_position_count():

    positions = [
        FakePosition(65, 25000, 25100),
        FakePosition(65, 25000, 24900),
    ]

    aggregator = PositionAggregator()

    assert aggregator.position_count(
        positions
    ) == 2


def test_calculate_exposure():

    positions = [
        FakePosition(65, 25000, 25100),
    ]

    aggregator = PositionAggregator()

    assert aggregator.exposure(
        positions
    ) == Decimal("1625000")


def test_unrealized_pnl():

    positions = [
        FakePosition(65, 25000, 25100),
    ]

    aggregator = PositionAggregator()

    assert aggregator.unrealized_pnl(
        positions
    ) == Decimal("6500")