from unittest.mock import Mock

import pytest

from brokers.dhan.client import DhanClient


def test_cancel_order_calls_sdk():
    sdk = Mock()

    sdk.cancel_order.return_value = {
        "status": "success",
    }

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    result = client.cancel_order("DHAN123")

    sdk.cancel_order.assert_called_once_with("DHAN123")

    assert result["status"] == "success"


def test_cancel_requires_sdk():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    with pytest.raises(RuntimeError):
        client.cancel_order("DHAN123")