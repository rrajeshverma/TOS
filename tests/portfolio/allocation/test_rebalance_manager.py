from portfolio.allocation.rebalance_manager import RebalanceManager


def test_rebalance_trigger():
    manager = RebalanceManager(threshold=10)

    assert manager.should_rebalance(
        50,
        70,
    )


def test_no_rebalance_below_threshold():
    manager = RebalanceManager(threshold=10)

    assert not manager.should_rebalance(
        50,
        55,
    )


def test_rebalance_execution():
    manager = RebalanceManager()

    result = manager.rebalance(
        50,
        80,
    )

    assert result["from"] == 50
    assert result["to"] == 80


def test_rebalance_history():
    manager = RebalanceManager()

    manager.rebalance(50, 80)

    assert manager.rebalance_count() == 1


def test_last_rebalance():
    manager = RebalanceManager()

    manager.rebalance(50, 80)

    assert manager.last_rebalance()["to"] == 80


def test_rebalance_report():
    manager = RebalanceManager()

    report = manager.report()

    assert report["threshold"] == 10


def test_custom_threshold():
    manager = RebalanceManager(threshold=5)

    assert manager.threshold == 5


def test_multiple_rebalances():
    manager = RebalanceManager()

    manager.rebalance(50, 60)
    manager.rebalance(60, 70)

    assert manager.rebalance_count() == 2


def test_empty_history():
    manager = RebalanceManager()

    assert manager.last_rebalance() is None


def test_report_history():
    manager = RebalanceManager()

    manager.rebalance(10, 20)

    assert len(manager.report()["history"]) == 1
