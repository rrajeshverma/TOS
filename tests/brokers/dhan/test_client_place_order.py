from unittest.mock import Mock

from brokers.dhan.client import DhanClient


def test_place_order_calls_sdk():
    sdk = Mock()

    sdk.place_order.return_value = {
        "orderId": "DHAN12345",
    }

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    order = {
        "security_id": "12345",
        "exchange_segment": "NSE_FNO",
        "transaction_type": "BUY",
        "quantity": 50,
    }

    result = client.place_order(order)

    sdk.place_order.assert_called_once_with(**order)

    assert result["orderId"] == "DHAN12345"


def test_place_order_requires_connection():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    try:
        client.place_order({})
    except RuntimeError:
        pass
    else:
        assert False