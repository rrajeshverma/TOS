from unittest.mock import Mock

from execution.order_service import OrderService


def test_place_order_calls_broker():
    broker = Mock()
    repository = Mock()

    broker.place_order.return_value = {"order_id": "ORD001"}

    service = OrderService(broker, repository)

    order = {"symbol": "NIFTY", "quantity": 65}

    result = service.place_order(order)

    broker.place_order.assert_called_once_with(order)
    repository.add.assert_called_once_with({"order_id": "ORD001"})
    assert result["order_id"] == "ORD001"