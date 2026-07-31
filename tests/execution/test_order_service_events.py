from execution.order_event_dispatcher import OrderEventDispatcher
from execution.order_events import OrderEventType
from execution.order_service import OrderService, OrderStatus


def test_submit_publishes_new_event():
    dispatcher = OrderEventDispatcher()
    received = []

    dispatcher.subscribe(received.append)

    service = OrderService(dispatcher=dispatcher)

    service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert len(received) == 1
    assert received[0].event_type is OrderEventType.NEW


def test_status_update_publishes_event():
    dispatcher = OrderEventDispatcher()
    received = []

    dispatcher.subscribe(received.append)

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit({"symbol": "NIFTY"})

    received.clear()

    service.update_status(
        order_id,
        OrderStatus.SUBMITTED,
    )

    assert len(received) == 1
    assert received[0].event_type is OrderEventType.SUBMITTED
