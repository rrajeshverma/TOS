from execution.trade_reconciliation import TradeReconciliation


def test_detect_missing_broker_trade():
    r = TradeReconciliation()

    r.add_local(
        "T1",
        65,
    )

    assert r.missing_broker_trades() == ["T1"]


def test_detect_extra_broker_trade():
    r = TradeReconciliation()

    r.add_broker(
        "T2",
        65,
    )

    assert r.extra_broker_trades() == ["T2"]


def test_reconciliation_report():
    r = TradeReconciliation()

    r.add_local(
        "T1",
        65,
    )

    r.add_broker(
        "T1",
        60,
    )

    report = r.reconciliation_report()

    assert report["reconciled"] is False
    assert report["differences"]["T1"] == 5
