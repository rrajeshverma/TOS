import pytest

from execution.order_recovery import OrderRecovery


class DummyBroker:
    def __init__(self, orders):
        self._orders = orders

    def get_orders(self):
        return self._orders


def test_add_order_increases_pending_count():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")

    assert recovery.pending_count() == 1
    assert recovery.has_pending_orders()


def test_remove_existing_order():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.remove_order("1")

    assert recovery.pending_count() == 0
    assert not recovery.has_pending_orders()


def test_remove_unknown_order_is_safe():
    recovery = OrderRecovery()

    recovery.remove_order("UNKNOWN")

    assert recovery.pending_count() == 0


def test_clear_removes_every_pending_order():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.add_order("2", "BANKNIFTY")

    recovery.clear()

    assert recovery.pending_count() == 0
    assert not recovery.has_pending_orders()


def test_get_unknown_order_returns_none():
    recovery = OrderRecovery()

    assert recovery.get_order("UNKNOWN") is None


def test_summary_returns_copy():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")

    summary = recovery.summary()

    summary["pending_orders"]["2"] = "BANKNIFTY"

    assert recovery.pending_count() == 1
    assert recovery.get_order("2") is None


def test_has_pending_orders_false_when_empty():
    recovery = OrderRecovery()

    assert recovery.has_pending_orders() is False


def test_has_pending_orders_true_after_add():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")

    assert recovery.has_pending_orders() is True


def test_pending_count_after_multiple_orders():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.add_order("2", "BANKNIFTY")
    recovery.add_order("3", "FINNIFTY")

    assert recovery.pending_count() == 3


def test_recover_without_broker_raises_runtime_error():
    recovery = OrderRecovery()

    with pytest.raises(RuntimeError):
        recovery.recover()


def test_sync_rebuilds_pending_orders():
    broker = DummyBroker(
        [
            {
                "order_id": "1",
                "symbol": "NIFTY",
                "status": "OPEN",
            },
            {
                "order_id": "2",
                "symbol": "BANKNIFTY",
                "status": "PENDING",
            },
        ]
    )

    recovery = OrderRecovery(broker=broker)

    recovery.sync()

    assert recovery.pending_count() == 2
    assert recovery.get_order("1") == "NIFTY"
    assert recovery.get_order("2") == "BANKNIFTY"


def test_sync_ignores_completed_orders():
    broker = DummyBroker(
        [
            {
                "order_id": "1",
                "symbol": "NIFTY",
                "status": "FILLED",
            },
            {
                "order_id": "2",
                "symbol": "BANKNIFTY",
                "status": "CANCELLED",
            },
            {
                "order_id": "3",
                "symbol": "FINNIFTY",
                "status": "REJECTED",
            },
        ]
    )

    recovery = OrderRecovery(broker=broker)

    recovery.sync()

    assert recovery.pending_count() == 0


def test_sync_replaces_previous_pending_orders():
    broker = DummyBroker(
        [
            {
                "order_id": "10",
                "symbol": "MIDCPNIFTY",
                "status": "OPEN",
            }
        ]
    )

    recovery = OrderRecovery(broker=broker)

    recovery.add_order("1", "OLD")

    recovery.sync()

    assert recovery.pending_count() == 1
    assert recovery.get_order("1") is None
    assert recovery.get_order("10") == "MIDCPNIFTY"


def test_sync_accepts_empty_broker_response():
    recovery = OrderRecovery(broker=DummyBroker([]))

    orders = recovery.sync()

    assert orders == []
    assert recovery.pending_count() == 0


def test_summary_pending_count_matches_internal_state():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.add_order("2", "BANKNIFTY")

    summary = recovery.summary()

    assert summary["pending_count"] == 2
    assert summary["has_pending"] is True
