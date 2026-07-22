from unittest.mock import Mock

import pytest

from brokers.dhan.client import DhanClient


def test_get_holdings_calls_sdk():
    sdk = Mock()

    sdk.get_holdings.return_value = [
        {
            "securityId": "500325",
            "quantity": 25,
        }
    ]

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    holdings = client.get_holdings()

    sdk.get_holdings.assert_called_once_with()

    assert len(holdings) == 1
    assert holdings[0]["securityId"] == "500325"


def test_get_holdings_requires_sdk():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    with pytest.raises(RuntimeError):
        client.get_holdings()
