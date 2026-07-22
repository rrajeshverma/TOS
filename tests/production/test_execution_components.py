from execution.order_recovery import OrderRecovery
from execution.order_repository import OrderRepository
from execution.position_synchronizer import PositionSynchronizer
from execution.trade_reconciliation import TradeReconciliation

# ---------------------------------------------------------------------
# OrderRecovery
# ---------------------------------------------------------------------


def test_order_recovery_initial_state():
    recovery = OrderRecovery()
    assert recovery.pending_count() == 0


def test_order_recovery_add_order():
    recovery = OrderRecovery()
    recovery.add_order("O1", "NIFTY")
    assert recovery.get_order("O1") == "NIFTY"


def test_order_recovery_remove_order():
    recovery = OrderRecovery()
    recovery.add_order("O1", "NIFTY")
    recovery.remove_order("O1")
    assert recovery.get_order("O1") is None


def test_order_recovery_has_pending_orders():
    recovery = OrderRecovery()
    recovery.add_order("O1", "BANKNIFTY")
    assert recovery.has_pending_orders() is True


def test_order_recovery_pending_count():
    recovery = OrderRecovery()
    recovery.add_order("1", "A")
    recovery.add_order("2", "B")
    assert recovery.pending_count() == 2


def test_order_recovery_clear():
    recovery = OrderRecovery()
    recovery.add_order("1", "A")
    recovery.clear()
    assert recovery.pending_count() == 0


def test_order_recovery_summary():
    recovery = OrderRecovery()
    recovery.add_order("1", "NIFTY")

    summary = recovery.summary()

    assert summary["pending_count"] == 1
    assert summary["has_pending"] is True


# ---------------------------------------------------------------------
# OrderRepository
# ---------------------------------------------------------------------


def test_order_repository_add():
    repo = OrderRepository()

    order = {
        "order_id": "101",
        "symbol": "NIFTY",
    }

    repo.add(order)

    assert repo.get("101") == order


def test_order_repository_missing():
    repo = OrderRepository()
    assert repo.get("XYZ") is None


def test_order_repository_overwrite():
    repo = OrderRepository()

    repo.add({"order_id": "1", "qty": 50})
    repo.add({"order_id": "1", "qty": 100})

    assert repo.get("1")["qty"] == 100


# ---------------------------------------------------------------------
# PositionSynchronizer
# ---------------------------------------------------------------------


class FakeBroker:

    def __init__(self, positions):
        self.positions = positions

    def get_positions(self):
        return self.positions


def test_position_synchronizer_empty():
    broker = FakeBroker([])
    sync = PositionSynchronizer(broker)

    assert sync.sync() == []


def test_position_synchronizer_single():
    broker = FakeBroker([{"symbol": "NIFTY", "qty": 50}])

    sync = PositionSynchronizer(broker)

    assert len(sync.sync()) == 1


def test_position_synchronizer_multiple():
    broker = FakeBroker(
        [
            {"symbol": "NIFTY"},
            {"symbol": "BANKNIFTY"},
        ]
    )

    sync = PositionSynchronizer(broker)

    assert len(sync.sync()) == 2


# ---------------------------------------------------------------------
# TradeReconciliation
# ---------------------------------------------------------------------


def test_trade_reconciliation_initial():
    rec = TradeReconciliation()
    assert rec.is_reconciled() is True


def test_trade_reconciliation_add_matching():
    rec = TradeReconciliation()

    rec.add_local("T1", 100)
    rec.add_broker("T1", 100)

    assert rec.is_reconciled() is True


def test_trade_reconciliation_difference():
    rec = TradeReconciliation()

    rec.add_local("T1", 150)
    rec.add_broker("T1", 100)

    assert rec.difference("T1") == 50


def test_trade_reconciliation_remove():
    rec = TradeReconciliation()

    rec.add_local("T1", 100)
    rec.remove_local("T1")

    assert rec.difference("T1") == 0


def test_trade_reconciliation_reset():
    rec = TradeReconciliation()

    rec.add_local("T1", 10)
    rec.add_broker("T1", 10)

    rec.reset()

    assert rec.is_reconciled() is True
    assert rec.summary()["local_trades"] == {}


def test_trade_reconciliation_summary():
    rec = TradeReconciliation()

    rec.add_local("T1", 25)
    rec.add_broker("T1", 25)

    summary = rec.summary()

    assert summary["reconciled"] is True
