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
