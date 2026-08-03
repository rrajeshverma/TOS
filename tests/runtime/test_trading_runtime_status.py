from runtime.trading_runtime import TradingRuntime


def create_runtime():
    return TradingRuntime({})


def test_status_returns_dictionary():
    assert isinstance(
        create_runtime().status(),
        dict,
    )


def test_status_contains_metrics():
    assert "metrics" in create_runtime().status()


def test_metrics_is_dictionary():
    assert isinstance(
        create_runtime().status()["metrics"],
        dict,
    )


def test_status_reports_orders_submitted():
    runtime = create_runtime()

    runtime.metrics.increment_orders_submitted()

    assert runtime.status()["metrics"]["orders_submitted"] == 1


def test_status_reports_orders_rejected():
    runtime = create_runtime()

    runtime.metrics.increment_orders_rejected()

    assert runtime.status()["metrics"]["orders_rejected"] == 1


def test_status_reports_guard_blocks():
    runtime = create_runtime()

    runtime.metrics.increment_guard_blocks()

    assert runtime.status()["metrics"]["guard_blocks"] == 1


def test_status_reports_reconnects():
    runtime = create_runtime()

    runtime.metrics.increment_reconnects()

    assert runtime.status()["metrics"]["reconnects"] == 1


def test_status_contains_required_sections():
    runtime = create_runtime()

    status = runtime.status()

    assert "status" in status
    assert "running" in status
    assert "metrics" in status


def test_status_is_repeatable():
    runtime = create_runtime()

    assert runtime.status() == runtime.status()


def test_status_never_returns_none():
    assert create_runtime().status() is not None
