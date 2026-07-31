from unittest.mock import MagicMock, patch

from brokers.clients.dhan_client import DhanClient


def test_client_created():
    client = DhanClient()

    assert client is not None
    assert client.sdk is not None


@patch("brokers.clients.dhan_client.dhanhq")
@patch("brokers.clients.dhan_client.DhanContext")
def test_get_fund_limits(mock_context, mock_dhanhq):
    sdk = MagicMock()
    sdk.get_fund_limits.return_value = {"funds": 1000}
    mock_dhanhq.return_value = sdk

    client = DhanClient()

    assert client.get_fund_limits() == {"funds": 1000}
    sdk.get_fund_limits.assert_called_once_with()


@patch("brokers.clients.dhan_client.dhanhq")
@patch("brokers.clients.dhan_client.DhanContext")
def test_get_positions(mock_context, mock_dhanhq):
    sdk = MagicMock()
    sdk.get_positions.return_value = ["POS1"]
    mock_dhanhq.return_value = sdk

    client = DhanClient()

    assert client.get_positions() == ["POS1"]
    sdk.get_positions.assert_called_once_with()


@patch("brokers.clients.dhan_client.dhanhq")
@patch("brokers.clients.dhan_client.DhanContext")
def test_get_holdings(mock_context, mock_dhanhq):
    sdk = MagicMock()
    sdk.get_holdings.return_value = ["HOLDING1"]
    mock_dhanhq.return_value = sdk

    client = DhanClient()

    assert client.get_holdings() == ["HOLDING1"]
    sdk.get_holdings.assert_called_once_with()


@patch("brokers.clients.dhan_client.dhanhq")
@patch("brokers.clients.dhan_client.DhanContext")
def test_get_orders(mock_context, mock_dhanhq):
    sdk = MagicMock()
    sdk.get_order_list.return_value = ["ORDER1"]
    mock_dhanhq.return_value = sdk

    client = DhanClient()

    assert client.get_orders() == ["ORDER1"]
    sdk.get_order_list.assert_called_once_with()
