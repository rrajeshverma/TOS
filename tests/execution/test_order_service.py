import pytest

from execution.order_service import OrderService


def test_order_service_starts_empty():
    service = OrderService()

    assert service.order_count == 0


def test_submit_order():
    service = OrderService()

    order = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 50,
    }

    order_id = service.submit(order)

    assert order_id == 1
    assert service.order_count == 1


def test_get_order():
    service = OrderService()

    order = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 50,
    }

    order_id = service.submit(order)

    assert service.get(order_id) == order


def test_get_unknown_order_returns_none():
    service = OrderService()

    assert service.get(999) is None


@pytest.mark.parametrize("count", [1, 2, 5])
def test_multiple_orders(count):
    service = OrderService()

    for i in range(count):
        service.submit(
            {
                "symbol": f"SYM{i}",
                "side": "BUY",
                "quantity": 10,
            }
        )

    assert service.order_count == count