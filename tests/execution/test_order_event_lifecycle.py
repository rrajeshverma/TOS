from execution.order_events import (
    OrderEvent,
    OrderEventType,
)
from execution.order_event_dispatcher import (
    OrderEventDispatcher,
)
from execution.order_status import OrderStatus


# -------------------------
# Order Event Tests
# -------------------------


def test_create_new_order_event():
    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.NEW,
    )

    assert event.order_id == 1
    assert event.event_type == OrderEventType.NEW


def test_event_contains_broker_order_id():
    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.SUBMITTED,
        broker_order_id="BRK001",
    )

    assert event.broker_order_id == "BRK001"


def test_event_without_broker_id():
    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.NEW,
    )

    assert event.broker_order_id is None


def test_order_event_types():
    assert OrderEventType.FILLED.value == "FILLED"
    assert OrderEventType.CANCELLED.value == "CANCELLED"


# -------------------------
# Dispatcher Tests
# -------------------------


def test_dispatcher_publish_event():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(lambda event: received.append(event))

    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.NEW,
    )

    dispatcher.publish(event)

    assert received[0] == event


def test_dispatcher_multiple_subscribers():
    dispatcher = OrderEventDispatcher()

    first = []
    second = []

    dispatcher.subscribe(lambda e: first.append(e))

    dispatcher.subscribe(lambda e: second.append(e))

    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.SUBMITTED,
    )

    dispatcher.publish(event)

    assert len(first) == 1
    assert len(second) == 1


def test_dispatcher_preserves_order():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(lambda e: received.append(e.event_type))

    dispatcher.publish(OrderEvent(1, OrderEventType.NEW))

    dispatcher.publish(OrderEvent(1, OrderEventType.FILLED))

    assert received == [
        OrderEventType.NEW,
        OrderEventType.FILLED,
    ]


def test_dispatcher_clear():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(lambda e: received.append(e))

    dispatcher.clear()

    dispatcher.publish(OrderEvent(1, OrderEventType.NEW))

    assert received == []


# -------------------------
# Order Status Tests
# -------------------------


def test_default_order_status():
    status = OrderStatus()

    assert status.state == "NEW"


def test_mark_submitted():
    status = OrderStatus()

    status.mark_submitted()

    assert status.state == "SUBMITTED"


def test_mark_filled():
    status = OrderStatus()

    status.mark_filled()

    assert status.state == "FILLED"


def test_mark_cancelled():
    status = OrderStatus()

    status.mark_cancelled()

    assert status.is_cancelled()


def test_open_status():
    status = OrderStatus()

    assert status.is_open()


def test_closed_status():
    status = OrderStatus()

    status.mark_filled()

    assert status.is_closed()


def test_status_reset():
    status = OrderStatus()

    status.mark_filled()

    status.reset()

    assert status.state == "NEW"
