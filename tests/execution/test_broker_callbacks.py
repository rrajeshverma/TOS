from unittest.mock import Mock

import pytest

from execution.order_service import OrderService, OrderStatus


def test_process_broker_callback_updates_status():
    dispatcher = Mock()

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 50,
        }
    )

    service.register_broker_order(order_id, "DH12345")

    dispatcher.publish.reset_mock()

    service.process_broker_callback(
        broker_order_id="DH12345",
        status=OrderStatus.SUBMITTED,
    )

    assert service.status(order_id) == OrderStatus.SUBMITTED
    assert dispatcher.publish.call_count == 1


def test_unknown_broker_order_id_raises_key_error():
    service = OrderService()

    with pytest.raises(KeyError):
        service.process_broker_callback(
            broker_order_id="UNKNOWN",
            status=OrderStatus.SUBMITTED,
        )


def test_duplicate_broker_callback_is_ignored():
    dispatcher = Mock()

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 50,
        }
    )

    service.register_broker_order(order_id, "DH12345")

    dispatcher.publish.reset_mock()

    service.process_broker_callback(
        "DH12345",
        OrderStatus.SUBMITTED,
    )

    assert dispatcher.publish.call_count == 1

    service.process_broker_callback(
        "DH12345",
        OrderStatus.SUBMITTED,
    )

    assert dispatcher.publish.call_count == 1