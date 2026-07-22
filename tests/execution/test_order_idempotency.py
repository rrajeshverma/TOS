from execution.order_idempotency import OrderIdempotency


def test_new_order_allowed():

    guard = OrderIdempotency()

    assert guard.is_duplicate(
        "NIFTY_BUY_25000"
    ) is False


def test_duplicate_order_blocked():

    guard = OrderIdempotency()

    guard.record(
        "NIFTY_BUY_25000"
    )

    assert guard.is_duplicate(
        "NIFTY_BUY_25000"
    ) is True
