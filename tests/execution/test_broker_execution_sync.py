from unittest.mock import Mock

from execution.broker_execution_sync import BrokerExecutionSync
from execution.execution_status import ExecutionStatus
from execution.order_events import OrderEventType


def create_sync():
    tracker = Mock()
    dispatcher = Mock()

    sync = BrokerExecutionSync(
        tracker,
        dispatcher,
    )

    return sync, tracker, dispatcher


def test_submit():
    sync, tracker, dispatcher = create_sync()

    sync.process(
        1,
        ExecutionStatus.SUBMITTED,
    )

    tracker.submit.assert_called_once_with(1)

    event = dispatcher.publish.call_args.args[0]

    assert event.order_id == 1
    assert event.event_type == OrderEventType.SUBMITTED


def test_partial_fill():
    sync, tracker, dispatcher = create_sync()

    sync.process(
        2,
        ExecutionStatus.PARTIALLY_FILLED,
    )

    tracker.partial_fill.assert_called_once_with(2)

    event = dispatcher.publish.call_args.args[0]

    assert event.event_type == OrderEventType.PARTIALLY_FILLED


def test_fill():
    sync, tracker, dispatcher = create_sync()

    sync.process(
        3,
        ExecutionStatus.FILLED,
    )

    tracker.fill.assert_called_once_with(3)

    event = dispatcher.publish.call_args.args[0]

    assert event.event_type == OrderEventType.FILLED


def test_cancel():
    sync, tracker, dispatcher = create_sync()

    sync.process(
        4,
        ExecutionStatus.CANCELLED,
    )

    tracker.cancel.assert_called_once_with(4)

    event = dispatcher.publish.call_args.args[0]

    assert event.event_type == OrderEventType.CANCELLED


def test_broker_order_id_forwarded():
    sync, _tracker, dispatcher = create_sync()

    sync.process(
        10,
        ExecutionStatus.SUBMITTED,
        broker_order_id="DHAN123",
    )

    event = dispatcher.publish.call_args.args[0]

    assert event.broker_order_id == "DHAN123"


def test_unknown_status_ignored():
    sync, tracker, dispatcher = create_sync()

    sync.process(
        5,
        ExecutionStatus.PENDING,
    )

    tracker.submit.assert_not_called()
    tracker.fill.assert_not_called()
    tracker.partial_fill.assert_not_called()
    tracker.cancel.assert_not_called()

    dispatcher.publish.assert_not_called()
