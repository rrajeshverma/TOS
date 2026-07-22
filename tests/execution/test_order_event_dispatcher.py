from execution.order_event_dispatcher import OrderEventDispatcher
from execution.order_events import OrderEvent, OrderEventType


def test_subscribe_and_publish():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(received.append)

    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.NEW,
    )

    dispatcher.publish(event)

    assert received == [event]


def test_multiple_subscribers():
    dispatcher = OrderEventDispatcher()

    first = []
    second = []

    dispatcher.subscribe(first.append)
    dispatcher.subscribe(second.append)

    event = OrderEvent(
        order_id=2,
        event_type=OrderEventType.SUBMITTED,
    )

    dispatcher.publish(event)

    assert first == [event]
    assert second == [event]


def test_clear_subscribers():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(received.append)

    dispatcher.clear()

    dispatcher.publish(
        OrderEvent(
            order_id=1,
            event_type=OrderEventType.NEW,
        )
    )

    assert received == []
