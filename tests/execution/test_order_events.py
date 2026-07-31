from execution.order_events import OrderEvent, OrderEventType


def test_create_order_event():
    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.SUBMITTED,
        broker_order_id="DHAN001",
    )

    assert event.order_id == 1
    assert event.event_type is OrderEventType.SUBMITTED
    assert event.broker_order_id == "DHAN001"


def test_order_event_is_frozen():
    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.NEW,
    )

    try:
        event.order_id = 10
    except Exception:
        pass
    else:
        assert False


def test_event_without_broker_id():
    event = OrderEvent(
        order_id=10,
        event_type=OrderEventType.CANCELLED,
    )

    assert event.broker_order_id is None
