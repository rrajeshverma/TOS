from recovery.order_recovery import (
    OrderRecoveryService,
)



def test_order_recovery_stores_order_state():

    recovery = OrderRecoveryService()


    state = recovery.recover(
        "ORDER001",
        {
            "status": "success",
            "orderId": "DHAN001",
        },
    )


    assert (
        state["order_id"]
        == "ORDER001"
    )

    assert (
        state["broker_order_id"]
        == "DHAN001"
    )



def test_recovered_order_can_be_loaded():

    recovery = OrderRecoveryService()


    recovery.recover(
        "ORDER001",
        {
            "status": "success",
            "orderId": "DHAN001",
        },
    )


    result = recovery.get(
        "ORDER001"
    )


    assert result is not None



def test_missing_order_returns_none():

    recovery = OrderRecoveryService()


    assert (
        recovery.get(
            "UNKNOWN"
        )
        is None
    )



def test_multiple_orders_are_recovered():

    recovery = OrderRecoveryService()


    recovery.recover(
        "ORDER001",
        {"status": "success"},
    )

    recovery.recover(
        "ORDER002",
        {"status": "pending"},
    )


    assert (
        recovery.count()
        == 2
    )



def test_clear_removes_recovery_state():

    recovery = OrderRecoveryService()


    recovery.recover(
        "ORDER001",
        {"status": "success"},
    )


    recovery.clear()


    assert (
        recovery.count()
        == 0
    )



def test_failed_broker_order_state_is_recovered():

    recovery = OrderRecoveryService()


    state = recovery.recover(
        "ORDER003",
        {
            "status": "failed",
            "orderId": None,
        },
    )


    assert (
        state["status"]
        == "failed"
    )
