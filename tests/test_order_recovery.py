from execution.order_recovery import OrderRecovery


def test_create_order_recovery():
    recovery = OrderRecovery()

    assert recovery.pending_orders == {}


def test_add_pending_order():
    recovery = OrderRecovery()

    recovery.add_order("ORD001", "NIFTY")

    assert recovery.pending_orders["ORD001"] == "NIFTY"


def test_remove_order():
    recovery = OrderRecovery()

    recovery.add_order("ORD001", "NIFTY")
    recovery.remove_order("ORD001")

    assert "ORD001" not in recovery.pending_orders


def test_has_pending_orders_true():
    recovery = OrderRecovery()

    recovery.add_order("ORD001", "NIFTY")

    assert recovery.has_pending_orders() is True


def test_has_pending_orders_false():
    recovery = OrderRecovery()

    assert recovery.has_pending_orders() is False


def test_pending_count():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.add_order("2", "BANKNIFTY")

    assert recovery.pending_count() == 2


def test_clear():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.clear()

    assert recovery.pending_orders == {}


def test_get_order():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")

    assert recovery.get_order("1") == "NIFTY"


def test_get_missing_order():
    recovery = OrderRecovery()

    assert recovery.get_order("ABC") is None


def test_summary():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")

    summary = recovery.summary()

    assert summary["pending_count"] == 1


def test_summary_has_pending():
    recovery = OrderRecovery()

    summary = recovery.summary()

    assert summary["has_pending"] is False


def test_duplicate_order_updates_symbol():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.add_order("1", "BANKNIFTY")

    assert recovery.pending_orders["1"] == "BANKNIFTY"


def test_reset_after_clear():
    recovery = OrderRecovery()

    recovery.add_order("1", "NIFTY")
    recovery.clear()

    assert recovery.pending_count() == 0


def test_remove_missing_order():
    recovery = OrderRecovery()

    recovery.remove_order("UNKNOWN")

    assert recovery.pending_count() == 0


def test_summary_contains_orders():
    recovery = OrderRecovery()

    summary = recovery.summary()

    assert "pending_orders" in summary
