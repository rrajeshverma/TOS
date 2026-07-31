from unittest.mock import Mock

from brokers.dhan_order_service import DhanOrderService


def test_created():
    service = DhanOrderService(Mock())

    assert service.client is not None


def test_client_saved():
    client = Mock()

    service = DhanOrderService(client)

    assert service.client is client


def test_get_positions_delegates():
    client = Mock()
    client.get_positions.return_value = []

    service = DhanOrderService(client)

    assert service.client.get_positions() == []


def test_get_orders_delegates():
    client = Mock()
    client.get_orders.return_value = []

    service = DhanOrderService(client)

    assert service.client.get_orders() == []

def test_get_holdings_delegates():
    client = Mock()
    client.get_holdings.return_value = []

    service = DhanOrderService(client)

    assert service.get_holdings() == []


def test_get_fund_limits_delegates():
    client = Mock()
    client.get_fund_limits.return_value = {"data": {}}

    service = DhanOrderService(client)

    assert service.get_fund_limits() == {"data": {}}

def test_place_order_delegates():
    client = Mock()
    client.place_order.return_value = {
        "orderId": "DHAN123",
    }

    service = DhanOrderService(client)

    result = service.place_order(
        security_id="1333",
        quantity=50,
    )

    assert result == {"orderId": "DHAN123"}

    client.place_order.assert_called_once_with(
        security_id="1333",
        quantity=50,
    )


def test_get_order_delegates():
    client = Mock()
    client.get_order.return_value = {
        "orderId": "123",
    }

    service = DhanOrderService(client)

    assert service.get_order("123") == {
        "orderId": "123",
    }

    client.get_order.assert_called_once_with("123")