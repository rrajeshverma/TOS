from execution.order_recovery import OrderRecovery
from execution.trade_reconciliation import TradeReconciliation


# ----------------------------
# Order Recovery Tests
# ----------------------------


def test_add_pending_order():

    recovery = OrderRecovery()

    recovery.add_order(
        "ORD001",
        "NIFTY",
    )

    assert recovery.get_order(
        "ORD001"
    ) == "NIFTY"


def test_pending_order_count():

    recovery = OrderRecovery()

    recovery.add_order(
        "ORD001",
        "NIFTY",
    )

    recovery.add_order(
        "ORD002",
        "BANKNIFTY",
    )

    assert recovery.pending_count() == 2


def test_has_pending_orders():

    recovery = OrderRecovery()

    assert recovery.has_pending_orders() is False

    recovery.add_order(
        "ORD001",
        "NIFTY",
    )

    assert recovery.has_pending_orders() is True


def test_remove_pending_order():

    recovery = OrderRecovery()

    recovery.add_order(
        "ORD001",
        "NIFTY",
    )

    recovery.remove_order(
        "ORD001"
    )

    assert recovery.get_order(
        "ORD001"
    ) is None


def test_remove_unknown_order_safe():

    recovery = OrderRecovery()

    recovery.remove_order(
        "UNKNOWN"
    )

    assert recovery.pending_count() == 0


def test_clear_all_pending_orders():

    recovery = OrderRecovery()

    recovery.add_order(
        "ORD001",
        "NIFTY",
    )

    recovery.clear()

    assert recovery.pending_count() == 0


def test_recovery_summary():

    recovery = OrderRecovery()

    recovery.add_order(
        "ORD001",
        "NIFTY",
    )

    summary = recovery.summary()

    assert summary["pending_count"] == 1
    assert summary["has_pending"] is True


# ----------------------------
# Trade Reconciliation Tests
# ----------------------------


def test_add_local_trade():

    recon = TradeReconciliation()

    recon.add_local(
        "T001",
        65,
    )

    assert recon.local_trades["T001"] == 65


def test_add_broker_trade():

    recon = TradeReconciliation()

    recon.add_broker(
        "T001",
        65,
    )

    assert recon.broker_trades["T001"] == 65


def test_trade_difference():

    recon = TradeReconciliation()

    recon.add_local(
        "T001",
        100,
    )

    recon.add_broker(
        "T001",
        80,
    )

    assert recon.difference(
        "T001"
    ) == 20


def test_reconciliation_success():

    recon = TradeReconciliation()

    recon.add_local(
        "T001",
        65,
    )

    recon.add_broker(
        "T001",
        65,
    )

    assert recon.is_reconciled() is True


def test_reconciliation_failure():

    recon = TradeReconciliation()

    recon.add_local(
        "T001",
        65,
    )

    recon.add_broker(
        "T001",
        60,
    )

    assert recon.is_reconciled() is False


def test_remove_local_trade():

    recon = TradeReconciliation()

    recon.add_local(
        "T001",
        65,
    )

    recon.remove_local(
        "T001"
    )

    assert "T001" not in recon.local_trades


def test_remove_broker_trade():

    recon = TradeReconciliation()

    recon.add_broker(
        "T001",
        65,
    )

    recon.remove_broker(
        "T001"
    )

    assert "T001" not in recon.broker_trades


def test_reconciliation_reset():

    recon = TradeReconciliation()

    recon.add_local(
        "T001",
        65,
    )

    recon.add_broker(
        "T001",
        65,
    )

    recon.reset()

    assert recon.local_trades == {}
    assert recon.broker_trades == {}