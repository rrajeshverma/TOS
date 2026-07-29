from unittest.mock import Mock

import pytest

from execution.order_service import OrderService, OrderStatus


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


def test_duplicate_status_update_does_not_publish_event():
    dispatcher = Mock()

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 1,
        }
    )

    # Ignore NEW event from submit()
    dispatcher.publish.reset_mock()

    service.update_status(order_id, OrderStatus.SUBMITTED)

    assert dispatcher.publish.call_count == 1

    # Duplicate update should not publish another event
    service.update_status(order_id, OrderStatus.SUBMITTED)

    assert dispatcher.publish.call_count == 1


def test_update_status_rejects_invalid_transition():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    service.update_status(
        order_id,
        OrderStatus.FILLED,
    )

    with pytest.raises(
        ValueError,
        match="Invalid status transition: FILLED -> CANCELLED",
    ):
        service.update_status(
            order_id,
            OrderStatus.CANCELLED,
        )
