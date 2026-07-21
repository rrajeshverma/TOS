from unittest.mock import Mock

import pytest

from brokers.dhan.client import DhanClient


def test_get_positions_calls_sdk():
    sdk = Mock()

    sdk.get_positions.return_value = [
        {
            "securityId": "12345",
            "quantity": 50,
        }
    ]

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    positions = client.get_positions()

    sdk.get_positions.assert_called_once_with()

    assert len(positions) == 1
    assert positions[0]["securityId"] == "12345"


def test_get_positions_requires_sdk():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    with pytest.raises(RuntimeError):
        client.get_positions()