from decimal import Decimal

from portfolio.portfolio_snapshot import PortfolioSnapshot
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

    assert aggregator.position_count(positions) == 2


def test_calculate_exposure():
    positions = [
        FakePosition(65, 25000, 25100),
    ]

    aggregator = PositionAggregator()

    assert aggregator.exposure(positions) == Decimal("1625000")


def test_unrealized_pnl():
    positions = [
        FakePosition(65, 25000, 25100),
    ]

    aggregator = PositionAggregator()

    assert aggregator.unrealized_pnl(positions) == Decimal("6500")


def test_position_count_none_returns_zero():
    aggregator = PositionAggregator()

    assert aggregator.position_count(None) == 0


def test_exposure_empty_positions():
    aggregator = PositionAggregator()

    assert aggregator.exposure([]) == Decimal("0")


def test_exposure_multiple_positions():
    positions = [
        FakePosition(65, 25000, 25100),
        FakePosition(50, 100, 110),
    ]

    aggregator = PositionAggregator()

    assert aggregator.exposure(positions) == Decimal("1630000")


def test_unrealized_pnl_empty_positions():
    aggregator = PositionAggregator()

    assert aggregator.unrealized_pnl([]) == Decimal("0")


def test_unrealized_pnl_multiple_positions():
    positions = [
        FakePosition(65, 25000, 25100),  # +6500
        FakePosition(50, 100, 90),  # -500
    ]

    aggregator = PositionAggregator()

    assert aggregator.unrealized_pnl(positions) == Decimal("6000")


def test_build_snapshot_returns_snapshot():
    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot([], Decimal("100000"))

    assert isinstance(snapshot, PortfolioSnapshot)


def test_build_snapshot_open_positions():
    positions = [
        FakePosition(65, 25000, 25100),
        FakePosition(50, 100, 100),
    ]

    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot(positions, Decimal("100000"))

    assert snapshot.open_positions == 2


def test_build_snapshot_unrealized_pnl():
    positions = [
        FakePosition(65, 25000, 25100),
    ]

    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot(
        positions,
        Decimal("100000"),
    )

    assert snapshot.unrealized_pnl == Decimal("6500")


def test_build_snapshot_realized_pnl():
    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot(
        [],
        Decimal("100000"),
        realized_pnl=Decimal("500"),
    )

    assert snapshot.realized_pnl == Decimal("500")


def test_build_snapshot_equity_without_positions():
    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot(
        [],
        Decimal("100000"),
    )

    assert snapshot.equity == Decimal("100000")


def test_build_snapshot_equity_with_realized_and_unrealized():
    positions = [
        FakePosition(65, 25000, 25100),  # +6500
    ]

    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot(
        positions,
        Decimal("100000"),
        realized_pnl=Decimal("500"),
    )

    assert snapshot.equity == Decimal("107000")


def test_build_snapshot_zero_open_positions():
    aggregator = PositionAggregator()

    snapshot = aggregator.build_snapshot(
        [],
        Decimal("100000"),
    )

    assert snapshot.open_positions == 0
