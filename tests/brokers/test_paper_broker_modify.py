from decimal import Decimal

import pytest

from brokers.models import (
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    ProductType,
)
from brokers.paper_broker import PaperBroker


def create_order():
    return Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=50,
        order_type=OrderType.LIMIT,
        product=ProductType.INTRADAY,
        price=Decimal(25000),
    )


def test_modify_price():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        price=Decimal(25100),
    )

    assert modified.price == Decimal(25100)


def test_modify_quantity():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        quantity=25,
    )

    assert modified.quantity == 25


def test_modify_trigger_price():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        trigger_price=Decimal(24950),
    )

    assert modified.trigger_price == Decimal(24950)


def test_modify_returns_updated_order():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        quantity=10,
    )

    assert modified.broker_order_id == order.broker_order_id


def test_modify_updates_storage():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    broker.modify_order(order.broker_order_id, quantity=15)

    stored = broker.get_order(order.broker_order_id)

    assert stored.quantity == 15


def test_modify_unknown_order():
    broker = PaperBroker()

    with pytest.raises(KeyError):
        broker.modify_order("UNKNOWN", quantity=5)


def test_modify_status_unchanged():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(order.broker_order_id, quantity=40)

    assert modified.status == OrderStatus.PENDING


def test_modify_symbol_unchanged():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(order.broker_order_id, quantity=5)

    assert modified.symbol == "NIFTY"


def test_modify_side_unchanged():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(order.broker_order_id, quantity=5)

    assert modified.side == OrderSide.BUY


def test_modify_order_type_unchanged():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(order.broker_order_id, quantity=5)

    assert modified.order_type == OrderType.LIMIT


def test_modify_product_unchanged():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(order.broker_order_id, quantity=5)

    assert modified.product == ProductType.INTRADAY


def test_multiple_modifications():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    broker.modify_order(order.broker_order_id, quantity=20)
    modified = broker.modify_order(
        order.broker_order_id,
        price=Decimal(25200),
    )

    assert modified.quantity == 20
    assert modified.price == Decimal(25200)


def test_modify_price_only():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        price=Decimal(24990),
    )

    assert modified.quantity == 50


def test_modify_quantity_only():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        quantity=5,
    )

    assert modified.price == Decimal(25000)


def test_modify_preserves_id():
    broker = PaperBroker()
    order = broker.place_order(create_order())

    modified = broker.modify_order(
        order.broker_order_id,
        quantity=30,
    )

    assert modified.broker_order_id == order.broker_order_id
