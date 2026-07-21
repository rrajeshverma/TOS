from unittest.mock import Mock

import pytest

from brokers.dhan.client import DhanClient


def test_get_order_calls_sdk():
    sdk = Mock()

    sdk.get_order.return_value = {
        "orderId": "DHAN123",
        "status": "FILLED",
    }

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    result = client.get_order("DHAN123")

    sdk.get_order.assert_called_once_with("DHAN123")

    assert result["orderId"] == "DHAN123"
    assert result["status"] == "FILLED"


def test_get_order_requires_sdk():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    with pytest.raises(RuntimeError):
        client.get_order("DHAN123")