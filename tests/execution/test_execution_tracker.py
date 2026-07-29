import pytest

from execution.execution_status import ExecutionStatus
from execution.execution_tracker import ExecutionTracker


ORDER_ID = "ORDER-1"


def create_tracker():
    tracker = ExecutionTracker()
    tracker.create(ORDER_ID)
    return tracker


def test_create_sets_pending_status():
    tracker = create_tracker()

    assert tracker.status(ORDER_ID) is ExecutionStatus.PENDING


def test_create_initializes_history():
    tracker = create_tracker()

    assert tracker.history(ORDER_ID) == [
        ExecutionStatus.PENDING,
    ]


def test_duplicate_create_raises():
    tracker = create_tracker()

    with pytest.raises(ValueError):
        tracker.create(ORDER_ID)


def test_submit_changes_status():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.SUBMITTED


def test_accept_changes_status():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.ACCEPTED


def test_partial_fill_changes_status():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)
    tracker.partial_fill(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.PARTIALLY_FILLED


def test_fill_from_accepted():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)
    tracker.fill(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.FILLED


def test_fill_from_partial_fill():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)
    tracker.partial_fill(ORDER_ID)
    tracker.fill(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.FILLED


def test_reject_changes_status():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.reject(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.REJECTED


def test_cancel_from_submitted():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.cancel(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.CANCELLED


def test_cancel_from_accepted():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)
    tracker.cancel(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.CANCELLED


def test_expire_changes_status():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.expire(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.EXPIRED


def test_pending_to_filled_is_invalid():
    tracker = create_tracker()

    with pytest.raises(ValueError):
        tracker.fill(ORDER_ID)


def test_pending_to_cancelled_is_invalid():
    tracker = create_tracker()

    with pytest.raises(ValueError):
        tracker.cancel(ORDER_ID)


def test_submitted_to_partial_fill_is_invalid():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)

    with pytest.raises(ValueError):
        tracker.partial_fill(ORDER_ID)


def test_filled_to_submitted_is_invalid():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)
    tracker.fill(ORDER_ID)

    with pytest.raises(ValueError):
        tracker.submit(ORDER_ID)


def test_rejected_to_filled_is_invalid():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.reject(ORDER_ID)

    with pytest.raises(ValueError):
        tracker.fill(ORDER_ID)


def test_cancelled_to_accepted_is_invalid():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.cancel(ORDER_ID)

    with pytest.raises(ValueError):
        tracker.accept(ORDER_ID)


def test_expired_to_submitted_is_invalid():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.expire(ORDER_ID)

    with pytest.raises(ValueError):
        tracker.submit(ORDER_ID)


def test_unknown_order_status_raises():
    tracker = ExecutionTracker()

    with pytest.raises(ValueError):
        tracker.status("UNKNOWN")


def test_unknown_order_history_raises():
    tracker = ExecutionTracker()

    with pytest.raises(ValueError):
        tracker.history("UNKNOWN")


def test_unknown_order_transition_raises():
    tracker = ExecutionTracker()

    with pytest.raises(ValueError):
        tracker.submit("UNKNOWN")


def test_exists_returns_true():
    tracker = create_tracker()

    assert tracker.exists(ORDER_ID)


def test_exists_returns_false():
    tracker = ExecutionTracker()

    assert not tracker.exists("UNKNOWN")


def test_history_records_all_transitions():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)
    tracker.partial_fill(ORDER_ID)
    tracker.fill(ORDER_ID)

    assert tracker.history(ORDER_ID) == [
        ExecutionStatus.PENDING,
        ExecutionStatus.SUBMITTED,
        ExecutionStatus.ACCEPTED,
        ExecutionStatus.PARTIALLY_FILLED,
        ExecutionStatus.FILLED,
    ]


def test_history_returns_copy():
    tracker = create_tracker()

    history = tracker.history(ORDER_ID)

    history.append(ExecutionStatus.FILLED)

    assert tracker.history(ORDER_ID) == [
        ExecutionStatus.PENDING,
    ]


def test_multiple_orders_are_independent():
    tracker = ExecutionTracker()

    tracker.create("ORDER-1")
    tracker.create("ORDER-2")

    tracker.submit("ORDER-1")

    assert tracker.status("ORDER-1") is ExecutionStatus.SUBMITTED

    assert tracker.status("ORDER-2") is ExecutionStatus.PENDING


def test_repeated_partial_fill_allowed():
    tracker = create_tracker()

    tracker.submit(ORDER_ID)
    tracker.accept(ORDER_ID)

    tracker.partial_fill(ORDER_ID)
    tracker.partial_fill(ORDER_ID)

    assert tracker.status(ORDER_ID) is ExecutionStatus.PARTIALLY_FILLED

    assert tracker.history(ORDER_ID) == [
        ExecutionStatus.PENDING,
        ExecutionStatus.SUBMITTED,
        ExecutionStatus.ACCEPTED,
        ExecutionStatus.PARTIALLY_FILLED,
        ExecutionStatus.PARTIALLY_FILLED,
    ]
