from execution.order_service import OrderService


def test_average_fill_price():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 100,
        }
    )

    service.record_fill(order_id, quantity=20, price=25000)
    service.record_fill(order_id, quantity=30, price=25010)
    service.record_fill(order_id, quantity=50, price=25020)

    assert service.average_fill_price(order_id) == 25013.0


def test_average_price_before_fill_is_zero():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 100,
        }
    )

    assert service.average_fill_price(order_id) == 0.0
