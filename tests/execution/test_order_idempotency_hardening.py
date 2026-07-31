from execution.order_idempotency import OrderIdempotency


def test_duplicate_after_record():
    tracker = OrderIdempotency()

    tracker.record("ABC")

    assert tracker.is_duplicate("ABC")


def test_clear_unknown_key_is_safe():
    tracker = OrderIdempotency()

    tracker.clear("UNKNOWN")

    assert tracker.count() == 0


def test_reset_clears_every_record():
    tracker = OrderIdempotency()

    tracker.record("1")
    tracker.record("2")
    tracker.record("3")

    tracker.reset()

    assert tracker.count() == 0


def test_get_unknown_returns_none():
    tracker = OrderIdempotency()

    assert tracker.get("UNKNOWN") is None


def test_record_none_result():
    tracker = OrderIdempotency()

    tracker.record("ABC")

    assert tracker.get("ABC") is None


def test_record_overwrites_existing_result():
    tracker = OrderIdempotency()

    tracker.record("ABC", "FIRST")
    tracker.record("ABC", "SECOND")

    assert tracker.get("ABC") == "SECOND"
    assert tracker.count() == 1
