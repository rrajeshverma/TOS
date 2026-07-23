from decimal import Decimal

import pytest

from engines.order_factory import OrderFactory
from shared.enums import Broker, OrderSide, OrderStatus

from tests.test_trade_factory import create_trade


def create_order():
    trade = create_trade()

    return OrderFactory().create(
        trade=trade,
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        price=Decimal("25000"),
    )


def test_order_factory_creates_order():
    order = create_order()

    assert order


def test_order_has_trade_reference():
    order = create_order()

    assert order.trade


def test_order_broker():
    order = create_order()

    assert order.broker == Broker.DHAN


def test_order_side():
    order = create_order()

    assert order.side == OrderSide.BUY


def test_order_quantity_from_trade():
    order = create_order()

    assert order.quantity == 65


def test_order_requested_price():
    order = create_order()

    assert order.requested_price == Decimal("25000")


def test_order_status_created():
    order = create_order()

    assert order.status == OrderStatus.CREATED


def test_order_has_generated_id():
    order = create_order()

    assert order.order_id
    assert isinstance(order.order_id, str)


def test_rejected_trade_not_allowed():
    with pytest.raises(ValueError):
        OrderFactory().create(
            trade=None,
            broker=Broker.DHAN,
            side=OrderSide.BUY,
            price=Decimal("25000"),
        )
