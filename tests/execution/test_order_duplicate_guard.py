from execution.order_duplicate_guard import (
    OrderDuplicateGuard,
)


def test_new_order_is_allowed():

    guard = OrderDuplicateGuard()

    assert (
        guard.can_submit("NIFTY_BUY_65")
        is True
    )



def test_registered_order_is_duplicate():

    guard = OrderDuplicateGuard()

    guard.register(
        "NIFTY_BUY_65"
    )

    assert (
        guard.is_duplicate(
            "NIFTY_BUY_65"
        )
        is True
    )



def test_duplicate_order_is_blocked():

    guard = OrderDuplicateGuard()

    key = "NIFTY_BUY_65"

    guard.register(key)

    assert (
        guard.can_submit(key)
        is False
    )



def test_different_order_is_allowed():

    guard = OrderDuplicateGuard()

    guard.register(
        "NIFTY_BUY_65"
    )

    assert (
        guard.can_submit(
            "NIFTY_SELL_65"
        )
        is True
    )



def test_clear_removes_duplicates():

    guard = OrderDuplicateGuard()

    guard.register(
        "NIFTY_BUY_65"
    )

    guard.clear()

    assert (
        guard.can_submit(
            "NIFTY_BUY_65"
        )
        is True
    )



def test_multiple_orders_are_tracked():

    guard = OrderDuplicateGuard()

    guard.register(
        "ORDER_1"
    )

    guard.register(
        "ORDER_2"
    )

    assert (
        guard.is_duplicate(
            "ORDER_1"
        )
        is True
    )

    assert (
        guard.is_duplicate(
            "ORDER_2"
        )
        is True
    )
