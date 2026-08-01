from runtime.runtime_metrics import RuntimeMetrics
from runtime.trading_runtime import TradingRuntime


def create_runtime():
    return TradingRuntime({})


def test_runtime_has_metrics():
    runtime = create_runtime()

    assert isinstance(
        runtime.metrics,
        RuntimeMetrics,
    )


def test_metrics_start_at_zero():
    runtime = create_runtime()

    snapshot = runtime.metrics.snapshot()

    assert snapshot["orders_submitted"] == 0
    assert snapshot["orders_rejected"] == 0
    assert snapshot["guard_blocks"] == 0
    assert snapshot["reconnects"] == 0


def test_runtime_metrics_are_available():
    runtime = create_runtime()

    assert runtime.metrics is not None


def test_runtime_metrics_snapshot():
    runtime = create_runtime()

    assert isinstance(
        runtime.metrics.snapshot(),
        dict,
    )


def test_runtime_metrics_are_independent():
    first = create_runtime()
    second = create_runtime()

    first.metrics.increment_orders_submitted()

    assert first.metrics.orders_submitted == 1
    assert second.metrics.orders_submitted == 0


def test_runtime_metrics_can_increment():
    runtime = create_runtime()

    runtime.metrics.increment_orders_submitted()

    assert runtime.metrics.orders_submitted == 1


def test_runtime_metrics_snapshot_updates():
    runtime = create_runtime()

    runtime.metrics.increment_guard_blocks()

    assert runtime.metrics.snapshot()["guard_blocks"] == 1


def test_runtime_metrics_reconnect_counter():
    runtime = create_runtime()

    runtime.metrics.increment_reconnects()

    assert runtime.metrics.reconnects == 1


def test_runtime_metrics_rejected_counter():
    runtime = create_runtime()

    runtime.metrics.increment_orders_rejected()

    assert runtime.metrics.orders_rejected == 1


def test_runtime_can_access_metrics_multiple_times():
    runtime = create_runtime()

    assert runtime.metrics is runtime.metrics
