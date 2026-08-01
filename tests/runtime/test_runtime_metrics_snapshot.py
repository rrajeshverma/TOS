from runtime.runtime_metrics import RuntimeMetrics


def create_metrics():
    return RuntimeMetrics()


def test_snapshot_returns_dict():
    assert isinstance(
        create_metrics().snapshot(),
        dict,
    )


def test_snapshot_contains_orders_submitted():
    assert "orders_submitted" in create_metrics().snapshot()


def test_snapshot_contains_orders_rejected():
    assert "orders_rejected" in create_metrics().snapshot()


def test_snapshot_contains_guard_blocks():
    assert "guard_blocks" in create_metrics().snapshot()


def test_snapshot_contains_reconnects():
    assert "reconnects" in create_metrics().snapshot()


def test_snapshot_reflects_submitted_orders():
    metrics = create_metrics()

    metrics.increment_orders_submitted()

    assert metrics.snapshot()["orders_submitted"] == 1


def test_snapshot_reflects_rejected_orders():
    metrics = create_metrics()

    metrics.increment_orders_rejected()

    assert metrics.snapshot()["orders_rejected"] == 1


def test_snapshot_reflects_guard_blocks():
    metrics = create_metrics()

    metrics.increment_guard_blocks()

    assert metrics.snapshot()["guard_blocks"] == 1


def test_snapshot_reflects_reconnects():
    metrics = create_metrics()

    metrics.increment_reconnects()

    assert metrics.snapshot()["reconnects"] == 1


def test_snapshot_has_four_entries():
    assert len(create_metrics().snapshot()) == 4
