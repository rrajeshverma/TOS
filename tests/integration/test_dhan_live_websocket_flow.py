"""
Integration Test:

Dhan Live WebSocket Flow

Flow:

Dhan Session
      |
      ▼
WebSocket Authentication
      |
      ▼
Connection
      |
      ▼
Subscription
      |
      ▼
Tick Pipeline
"""

from datetime import datetime


from brokers.dhan.session import DhanSession
from brokers.dhan.websocket import WebSocketClient



class DummyWebSocketTransport:

    def __init__(self):
        self.connected = False
        self.authenticated = False
        self.messages = []
        self.subscriptions = []

    def authenticate(
        self,
        token,
    ):
        self.authenticated = True
        self.token = token

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def subscribe(
        self,
        symbol,
    ):
        self.subscriptions.append(
            symbol
        )

    def send(
        self,
        message,
    ):
        self.messages.append(
            message
        )

def create_websocket():

    session = DhanSession()

    session.authenticate(
        "TEST_TOKEN"
    )

    transport = DummyWebSocketTransport()

    client = WebSocketClient(
        transport,
        session,
    )

    return client, transport


def test_websocket_authentication():

    client, transport = create_websocket()

    client.connect()

    assert transport.authenticated is True


def test_websocket_connects_with_authenticated_session():

    client, transport = create_websocket()

    client.connect()

    assert transport.connected is True


def test_websocket_subscribes_symbol():

    client, _ = create_websocket()

    client.connect()

    client.subscribe(
        "NIFTY"
    )

    assert (
        "NIFTY"
        in client.subscriptions
    )


def test_websocket_receives_tick():

    received = []

    client, _ = create_websocket()

    client.register_tick_callback(
        lambda tick: received.append(
            tick
        )
    )

    client.emit_tick(
        {
            "symbol": "NIFTY",
            "ltp": 25000,
            "volume": 1000,
            "timestamp": datetime.now(),
        }
    )

    assert len(received) == 1


def test_websocket_disconnect_flow():

    client, transport = create_websocket()

    client.connect()

    client.disconnect()

    assert transport.connected is False