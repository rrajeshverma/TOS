from execution.order_service import OrderService


def test_modify_order_quantity():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 100,
        }
    )

    service.modify_order(order_id, quantity=150)

    assert service.order(order_id)["quantity"] == 150