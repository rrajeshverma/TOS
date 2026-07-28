from monitoring.metrics_collector import (
    MetricsCollector,
)



def test_metrics_start_zero():

    metrics = MetricsCollector()


    assert (
        metrics.get(
            "orders"
        )
        == 0
    )



def test_increment_order_metric():

    metrics = MetricsCollector()


    metrics.increment(
        "orders"
    )


    assert (
        metrics.get(
            "orders"
        )
        == 1
    )



def test_multiple_metrics_are_tracked():

    metrics = MetricsCollector()


    metrics.increment(
        "orders"
    )

    metrics.increment(
        "successful_orders"
    )

    metrics.increment(
        "recoveries"
    )


    snapshot = metrics.snapshot()


    assert (
        snapshot["orders"]
        == 1
    )

    assert (
        snapshot["successful_orders"]
        == 1
    )

    assert (
        snapshot["recoveries"]
        == 1
    )



def test_unknown_metric_is_rejected():

    metrics = MetricsCollector()


    try:

        metrics.increment(
            "unknown"
        )

        assert False

    except ValueError as exc:

        assert (
            str(exc)
            == "Unknown metric: unknown"
        )



def test_snapshot_returns_copy():

    metrics = MetricsCollector()


    metrics.increment(
        "orders"
    )


    snapshot = metrics.snapshot()

    snapshot["orders"] = 100


    assert (
        metrics.get(
            "orders"
        )
        == 1
    )



def test_reset_clears_metrics():

    metrics = MetricsCollector()


    metrics.increment(
        "orders"
    )

    metrics.increment(
        "failed_orders"
    )


    metrics.reset()


    assert (
        metrics.get(
            "orders"
        )
        == 0
    )

    assert (
        metrics.get(
            "failed_orders"
        )
        == 0
    )
