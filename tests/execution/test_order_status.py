from execution.order_service import OrderService, OrderStatus


def test_new_order_status():
    service = OrderService()

    order = {"symbol": "NIFTY", "quantity": 65}

    order_id = service.submit(order)

    assert service.status(order_id) == OrderStatus.NEW


def test_update_order_status():
    service = OrderService()

    order = {"symbol": "NIFTY", "quantity": 65}

    order_id = service.submit(order)

    service.update_status(order_id, OrderStatus.SUBMITTED)

    assert service.status(order_id) == OrderStatus.SUBMITTED


def test_unknown_order_status():
    service = OrderService()

    assert service.status(999) is None
