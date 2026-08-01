from runtime.runtime_metrics import RuntimeMetrics


def test_metrics_start_at_zero():
    metrics = RuntimeMetrics()

    assert metrics.orders_submitted == 0
    assert metrics.orders_rejected == 0
    assert metrics.guard_blocks == 0
    assert metrics.reconnects == 0


def test_increment_orders_submitted():
    metrics = RuntimeMetrics()

    metrics.increment_orders_submitted()

    assert metrics.orders_submitted == 1


def test_increment_orders_rejected():
    metrics = RuntimeMetrics()

    metrics.increment_orders_rejected()

    assert metrics.orders_rejected == 1


def test_increment_guard_blocks():
    metrics = RuntimeMetrics()

    metrics.increment_guard_blocks()

    assert metrics.guard_blocks == 1


def test_increment_reconnects():
    metrics = RuntimeMetrics()

    metrics.increment_reconnects()

    assert metrics.reconnects == 1


def test_multiple_submitted_orders():
    metrics = RuntimeMetrics()

    for _ in range(5):
        metrics.increment_orders_submitted()

    assert metrics.orders_submitted == 5


def test_multiple_rejected_orders():
    metrics = RuntimeMetrics()

    for _ in range(3):
        metrics.increment_orders_rejected()

    assert metrics.orders_rejected == 3


def test_multiple_guard_blocks():
    metrics = RuntimeMetrics()

    for _ in range(4):
        metrics.increment_guard_blocks()

    assert metrics.guard_blocks == 4


def test_multiple_reconnects():
    metrics = RuntimeMetrics()

    for _ in range(2):
        metrics.increment_reconnects()

    assert metrics.reconnects == 2


def test_metrics_are_independent():
    first = RuntimeMetrics()
    second = RuntimeMetrics()

    first.increment_orders_submitted()

    assert first.orders_submitted == 1
    assert second.orders_submitted == 0
