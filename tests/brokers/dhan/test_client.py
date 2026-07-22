import pytest

from brokers.dhan.client import DhanClient


def test_client_stores_credentials():
    client = DhanClient(
        client_id="client123",
        access_token="token123",
    )

    assert client.client_id == "client123"
    assert client.access_token == "token123"


def test_client_is_disconnected_initially():
    client = DhanClient(
        client_id="client123",
        access_token="token123",
    )

    assert client.connected is False


def test_connect_sets_connected():
    client = DhanClient(
        client_id="client123",
        access_token="token123",
    )

    client.connect()

    assert client.connected is True


def test_disconnect_sets_disconnected():
    client = DhanClient(
        client_id="client123",
        access_token="token123",
    )

    client.connect()
    client.disconnect()

    assert client.connected is False


def test_double_connect_is_safe():
    client = DhanClient(
        client_id="client123",
        access_token="token123",
    )

    client.connect()
    client.connect()

    assert client.connected is True


def test_double_disconnect_is_safe():
    client = DhanClient(
        client_id="client123",
        access_token="token123",
    )

    client.disconnect()
    client.disconnect()

    assert client.connected is False
