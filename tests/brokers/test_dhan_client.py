from unittest.mock import Mock, patch

from brokers.clients.dhan_client import DhanClient


def test_dhan_client_created():

    with patch("brokers.clients.dhan_client.dhanhq"):

        client = DhanClient()

        assert client is not None


def test_sdk_property():

    with patch("brokers.clients.dhan_client.dhanhq") as sdk:

        client = DhanClient()

        assert client.sdk == sdk.return_value


def test_get_fund_limits():

    with patch("brokers.clients.dhan_client.dhanhq") as sdk:

        sdk.return_value.get_fund_limits.return_value = {
            "data": {}
        }

        client = DhanClient()

        result = client.get_fund_limits()

        assert result == {
            "data": {}
        }


def test_get_positions():

    with patch("brokers.clients.dhan_client.dhanhq") as sdk:

        sdk.return_value.get_positions.return_value = []

        client = DhanClient()

        assert client.get_positions() == []


def test_get_holdings():

    with patch("brokers.clients.dhan_client.dhanhq") as sdk:

        sdk.return_value.get_holdings.return_value = []

        client = DhanClient()

        assert client.get_holdings() == []


def test_get_orders():

    with patch("brokers.clients.dhan_client.dhanhq") as sdk:

        sdk.return_value.get_order_list.return_value = []

        client = DhanClient()

        assert client.get_orders() == []