from execution.order_service import OrderService, OrderStatus


def test_partial_fill_updates_status():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 100,
        }
    )

    service.record_fill(order_id, 25)

    assert service.filled_quantity(order_id) == 25
    assert service.remaining_quantity(order_id) == 75
    assert service.status(order_id) == OrderStatus.PARTIALLY_FILLED


def test_final_fill_marks_order_filled():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 100,
        }
    )

    service.record_fill(order_id, 40)
    service.record_fill(order_id, 60)

    assert service.filled_quantity(order_id) == 100
    assert service.remaining_quantity(order_id) == 0
    assert service.status(order_id) == OrderStatus.FILLED


import pytest


def test_cannot_overfill_order():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 100,
        }
    )

    service.record_fill(order_id, 100)

    with pytest.raises(ValueError):
        service.record_fill(order_id, 1)
