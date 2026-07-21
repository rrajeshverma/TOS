from unittest.mock import Mock

import pytest

from brokers.dhan.client import DhanClient


def test_get_funds_calls_sdk():
    sdk = Mock()

    sdk.get_funds.return_value = {
        "availableBalance": 250000.00,
        "utilizedMargin": 50000.00,
    }

    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    client._sdk = sdk

    funds = client.get_funds()

    sdk.get_funds.assert_called_once_with()

    assert funds["availableBalance"] == 250000.00
    assert funds["utilizedMargin"] == 50000.00


def test_get_funds_requires_sdk():
    client = DhanClient(
        client_id="client",
        access_token="token",
    )

    with pytest.raises(RuntimeError):
        client.get_funds()