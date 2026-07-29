from datetime import datetime

from execution.execution_status import ExecutionStatus
from execution.order_event import OrderEvent


def test_order_event_creation():
    event = OrderEvent(
        order_id="ORD-1",
        status=ExecutionStatus.SUBMITTED,
    )

    assert event.order_id == "ORD-1"
    assert event.status is ExecutionStatus.SUBMITTED


def test_timestamp_created():
    event = OrderEvent(
        order_id="ORD-1",
        status=ExecutionStatus.SUBMITTED,
    )

    assert isinstance(
        event.timestamp,
        datetime,
    )


def test_optional_fields():
    event = OrderEvent(
        order_id="ORD-1",
        status=ExecutionStatus.FILLED,
        broker_order_id="BRK-123",
        message="Filled",
        quantity=50,
        price=24875.5,
    )

    assert event.broker_order_id == "BRK-123"
    assert event.message == "Filled"
    assert event.quantity == 50
    assert event.price == 24875.5


def test_event_is_frozen():
    event = OrderEvent(
        order_id="ORD-1",
        status=ExecutionStatus.SUBMITTED,
    )

    try:
        event.order_id = "NEW"
        assert False
    except Exception:
        assert True


def test_events_equal():
    ts = datetime.now()

    a = OrderEvent(
        order_id="1",
        status=ExecutionStatus.SUBMITTED,
        timestamp=ts,
    )

    b = OrderEvent(
        order_id="1",
        status=ExecutionStatus.SUBMITTED,
        timestamp=ts,
    )

    assert a == b
