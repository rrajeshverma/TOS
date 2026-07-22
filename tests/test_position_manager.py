from decimal import Decimal

from domain.position import Position
from services.position_manager import PositionManager
from shared.enums import TradeStatus


def test_open_position():

    manager = PositionManager()

    position = manager.open_position(
        order=None,
        quantity=65,
        price=Decimal("25000"),
    )

    assert position.quantity == 65
    assert position.average_price == Decimal("25000")
    assert position.last_traded_price == Decimal("25000")
    assert position.status == TradeStatus.OPEN


def test_update_price():

    manager = PositionManager()

    position = manager.open_position(
        order=None,
        quantity=65,
        price=Decimal("25000"),
    )

    updated = manager.update_price(
        position,
        Decimal("25050"),
    )

    assert updated.last_traded_price == Decimal("25050")


def test_unrealized_pnl():

    manager = PositionManager()

    position = manager.open_position(
        order=None,
        quantity=65,
        price=Decimal("25000"),
    )

    updated = manager.update_price(
        position,
        Decimal("25020"),
    )

    pnl = manager.unrealized_pnl(updated)

    assert pnl == Decimal("1300")


def test_close_position():

    manager = PositionManager()

    position = manager.open_position(
        order=None,
        quantity=65,
        price=Decimal("25000"),
    )

    closed = manager.close_position(
        position,
        Decimal("25100"),
    )

    assert closed.status == TradeStatus.CLOSED


def test_is_position_open():
    manager = PositionManager()

    position = Position(
        position_id="POS001",
        order=None,
        quantity=1,
        average_price=Decimal("100"),
        last_traded_price=Decimal("100"),
        status=TradeStatus.OPEN,
        opened_at=None,
        closed_at=None,
    )

    assert manager.is_position_open(position) is True
