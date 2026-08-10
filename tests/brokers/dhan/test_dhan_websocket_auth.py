"""
Tests:
Dhan WebSocket authentication lifecycle
"""

import pytest

from brokers.dhan.session import DhanSession
from brokers.dhan.websocket import WebSocketClient


class DummyWebSocketTransport:
    """
    Fake Dhan websocket transport.
    """

    def __init__(self):
        self.connected = False
        self.token = None
        self.subscriptions = []

    def authenticate(
        self,
        token,
    ):
        self.token = token

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def subscribe(
        self,
        symbol,
    ):
        self.subscriptions.append(symbol)


def create_websocket_client():
    session = DhanSession()

    transport = DummyWebSocketTransport()

    client = WebSocketClient(
        transport,
        session,
    )

    return client, session, transport


def test_websocket_requires_authentication():
    client, _, _ = create_websocket_client()

    with pytest.raises(RuntimeError):
        client.connect()


def test_websocket_authentication():
    client, session, transport = create_websocket_client()

    session.authenticate("ACCESS_TOKEN")

    client.connect()

    assert transport.connected is True
    assert transport.token == "ACCESS_TOKEN"


def test_websocket_disconnect():
    client, session, _ = create_websocket_client()

    session.authenticate("ACCESS_TOKEN")

    client.connect()

    client.disconnect()

    assert client.is_connected is False


def test_websocket_subscription_after_authentication():
    client, session, transport = create_websocket_client()

    session.authenticate("ACCESS_TOKEN")

    client.connect()

    client.subscribe("NIFTY")

    assert "NIFTY" in transport.subscriptions
