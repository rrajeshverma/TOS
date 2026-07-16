from execution.order_repository import OrderRepository


def test_add_and_get_order():
    repo = OrderRepository()

    order = {
        "order_id": "ORD001",
        "symbol": "NIFTY",
        "quantity": 65,
    }

    repo.add(order)

    assert repo.get("ORD001") == order