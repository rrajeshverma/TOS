from types import SimpleNamespace

import pytest

from execution.order_repository import OrderRepository


def test_add_and_get_order():
    repo = OrderRepository()

    order = {
        "order_id": "ORD001",
        "symbol": "NIFTY",
        "quantity": 65,
    }

    repo.add(order)

    assert repo.get("ORD001") == order


def test_add_object_with_order_id():
    repo = OrderRepository()

    order = SimpleNamespace(
        order_id="ORD002",
        symbol="NIFTY",
        quantity=65,
    )

    repo.add(order)

    assert repo.get("ORD002") is order


def test_add_invalid_order_raises_value_error():
    repo = OrderRepository()

    with pytest.raises(ValueError, match="Invalid order type"):
        repo.add(object())


def test_exists():
    repo = OrderRepository()

    repo.add({"order_id": "ORD001"})

    assert repo.exists("ORD001")
    assert not repo.exists("ORD999")


def test_remove():
    repo = OrderRepository()

    repo.add({"order_id": "ORD001"})

    repo.remove("ORD001")

    assert repo.get("ORD001") is None


def test_all():
    repo = OrderRepository()

    order1 = {"order_id": "ORD001"}
    order2 = {"order_id": "ORD002"}

    repo.add(order1)
    repo.add(order2)

    assert repo.all() == [order1, order2]


def test_count():
    repo = OrderRepository()

    repo.add({"order_id": "ORD001"})
    repo.add({"order_id": "ORD002"})

    assert repo.count == 2


def test_remove_unknown_order_is_safe():
    repo = OrderRepository()

    repo.remove("UNKNOWN")

    assert repo.count == 0


def test_add_broker_order_uses_broker_order_id():
    from brokers.models import Order, OrderSide, OrderType, ProductType

    repo = OrderRepository()

    order = Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=15,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
        broker_order_id="BROKER001",
    )

    repo.add(order)

    assert repo.get("BROKER001") is order
