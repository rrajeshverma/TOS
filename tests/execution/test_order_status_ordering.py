from execution.order_service import OrderService, OrderStatus


def test_stale_status_update_is_ignored():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 50,
        }
    )

    service.update_status(order_id, OrderStatus.SUBMITTED)
    service.update_status(order_id, OrderStatus.FILLED)

    # Old callback arrives late
    service.update_status(order_id, OrderStatus.SUBMITTED)

    assert service.status(order_id) == OrderStatus.FILLED