import pytest

from execution.order_service import OrderService, OrderStatus


def test_cancel_existing_order():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert service.cancel_order(order_id) is True
    assert service.status(order_id) == OrderStatus.CANCELLED


def test_cancel_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.cancel_order(999)