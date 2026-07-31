from unittest.mock import Mock

import pytest

from brokers.dhan.client import DhanClient


def test_modify_order_calls_sdk():
    sdk = Mock()

    sdk.modify_order.return_value = {
        "status": "success",
    }

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    updates = {
        "quantity": 100,
        "price": 24550.25,
    }

    result = client.modify_order(
        "DHAN123",
        updates,
    )

    sdk.modify_order.assert_called_once_with(
        "DHAN123",
        **updates,
    )

    assert result["status"] == "success"


def test_modify_requires_sdk():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    with pytest.raises(RuntimeError):
        client.modify_order(
            "DHAN123",
            {},
        )
