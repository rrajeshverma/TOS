from execution.trade_reconciliation import TradeReconciliation


def test_create_trade_reconciliation():
    reconciliation = TradeReconciliation()

    assert reconciliation.local_trades == {}
    assert reconciliation.broker_trades == {}


def test_add_local_trade():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)

    assert reconciliation.local_trades["T1"] == 1


def test_add_broker_trade():
    reconciliation = TradeReconciliation()

    reconciliation.add_broker("T1", 1)

    assert reconciliation.broker_trades["T1"] == 1


def test_trades_match():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)
    reconciliation.add_broker("T1", 1)

    assert reconciliation.is_reconciled() is True


def test_trades_do_not_match():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)
    reconciliation.add_broker("T1", 2)

    assert reconciliation.is_reconciled() is False


def test_difference():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 3)
    reconciliation.add_broker("T1", 1)

    assert reconciliation.difference("T1") == 2


def test_missing_trade():
    reconciliation = TradeReconciliation()

    assert reconciliation.difference("UNKNOWN") == 0


def test_remove_local_trade():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)
    reconciliation.remove_local("T1")

    assert "T1" not in reconciliation.local_trades


def test_remove_broker_trade():
    reconciliation = TradeReconciliation()

    reconciliation.add_broker("T1", 1)
    reconciliation.remove_broker("T1")

    assert "T1" not in reconciliation.broker_trades


def test_reset():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)
    reconciliation.add_broker("T1", 1)

    reconciliation.reset()

    assert reconciliation.local_trades == {}
    assert reconciliation.broker_trades == {}


def test_summary_contains_local():
    reconciliation = TradeReconciliation()

    assert "local_trades" in reconciliation.summary()


def test_summary_contains_broker():
    reconciliation = TradeReconciliation()

    assert "broker_trades" in reconciliation.summary()


def test_summary_contains_status():
    reconciliation = TradeReconciliation()

    assert "reconciled" in reconciliation.summary()


def test_multiple_trades():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)
    reconciliation.add_local("T2", 2)

    reconciliation.add_broker("T1", 1)
    reconciliation.add_broker("T2", 2)

    assert reconciliation.is_reconciled() is True


def test_negative_difference():
    reconciliation = TradeReconciliation()

    reconciliation.add_local("T1", 1)
    reconciliation.add_broker("T1", 3)

    assert reconciliation.difference("T1") == -2
