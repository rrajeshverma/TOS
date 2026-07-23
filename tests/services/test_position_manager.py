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
