from datetime import datetime
from decimal import Decimal

from engines.order_factory import OrderFactory
from services.position_manager import PositionManager
from shared.enums import Broker, OrderSide, TradeStatus

from tests.test_trade_factory import create_trade


def create_order():
    return OrderFactory().create(
        trade=create_trade(),
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        price=Decimal("25000"),
    )


def create_position():
    order = create_order()

    return PositionManager().open_position(
        order=order,
        quantity=order.quantity,
        price=order.requested_price,
    )


# ---------------------------------------------------------
# Creation
# ---------------------------------------------------------


def test_position_created():
    position = create_position()

    assert position


def test_position_has_order_reference():
    position = create_position()

    assert position.order


def test_position_quantity():
    position = create_position()

    assert position.quantity == 65


def test_position_average_price():
    position = create_position()

    assert position.average_price == Decimal("25000")


def test_position_last_price():
    position = create_position()

    assert position.last_traded_price == Decimal("25000")


def test_position_status_open():
    position = create_position()

    assert position.status == TradeStatus.OPEN


# ---------------------------------------------------------
# Properties
# ---------------------------------------------------------


def test_position_is_open():
    position = create_position()

    assert position.is_open


def test_position_not_closed():
    position = create_position()

    assert not position.is_closed


# ---------------------------------------------------------
# Price update
# ---------------------------------------------------------


def test_update_price():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.last_traded_price == Decimal("25100")


def test_update_price_preserves_quantity():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.quantity == 65


# ---------------------------------------------------------
# PNL
# ---------------------------------------------------------


def test_unrealized_pnl():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert PositionManager.unrealized_pnl(updated) == Decimal("6500")


def test_realized_pnl():
    pnl = PositionManager.realized_pnl(
        Decimal("25000"),
        Decimal("25100"),
        65,
    )

    assert pnl == Decimal("6500")


# ---------------------------------------------------------
# Closing
# ---------------------------------------------------------


def test_close_position():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert closed.status == TradeStatus.CLOSED


def test_closed_position_has_time():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert isinstance(
        closed.closed_at,
        datetime,
    )


def test_closed_position_not_open():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert not closed.is_open


# ---------------------------------------------------------
# Additional Certification Tests
# ---------------------------------------------------------


def test_open_position_generates_position_id():
    position = create_position()

    assert position.position_id


def test_open_position_sets_opened_at():
    position = create_position()

    assert isinstance(position.opened_at, datetime)


def test_open_position_accepts_none_order():
    position = PositionManager().open_position(
        order=None,
        quantity=10,
        price=Decimal("100"),
    )

    assert position.order is None
    assert position.quantity == 10
    assert position.status == TradeStatus.OPEN


def test_update_price_preserves_position_id():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.position_id == position.position_id


def test_update_price_preserves_average_price():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.average_price == position.average_price


def test_update_price_preserves_order_reference():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.order == position.order


def test_update_price_preserves_opened_at():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.opened_at == position.opened_at


def test_update_price_preserves_status():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated.status == position.status


def test_update_price_returns_new_instance():
    position = create_position()

    updated = PositionManager.update_price(
        position,
        Decimal("25100"),
    )

    assert updated is not position


def test_close_position_preserves_position_id():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert closed.position_id == position.position_id


def test_close_position_preserves_order_reference():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert closed.order == position.order


def test_close_position_preserves_opened_at():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert closed.opened_at == position.opened_at


def test_close_position_returns_new_instance():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert closed is not position


def test_is_position_open_true():
    position = create_position()

    assert PositionManager.is_position_open(position)


def test_is_position_open_false():
    position = create_position()

    closed = PositionManager.close_position(
        position,
        Decimal("25100"),
    )

    assert not PositionManager.is_position_open(closed)
