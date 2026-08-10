"""
Tests:
Dhan WebSocket tick subscription flow
"""

from brokers.dhan.models import BrokerTick
from brokers.dhan.session import DhanSession
from brokers.dhan.websocket import WebSocketClient


class DummyTickTransport:
    """
    Fake websocket transport.
    """

    def __init__(self):
        self.auth_token = None
        self.connected = False
        self.subscribed = []

    def authenticate(
        self,
        token,
    ):
        self.auth_token = token

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def subscribe(
        self,
        symbol,
    ):
        self.subscribed.append(symbol)


def create_client():
    session = DhanSession()

    session.authenticate("ACCESS_TOKEN")

    transport = DummyTickTransport()

    client = WebSocketClient(
        transport,
        session,
    )

    return client, transport


def test_tick_subscription_requires_connection():
    client, _ = create_client()

    try:
        client.subscribe("NIFTY")
    except RuntimeError:
        assert True
    else:
        assert False


def test_subscribe_nifty_after_connection():
    client, transport = create_client()

    client.connect()

    client.subscribe("NIFTY")

    assert "NIFTY" in transport.subscribed


def test_multiple_symbol_subscription():
    client, transport = create_client()

    client.connect()

    client.subscribe("NIFTY")
    client.subscribe("BANKNIFTY")

    assert "NIFTY" in transport.subscribed
    assert "BANKNIFTY" in transport.subscribed


def test_tick_callback_receives_market_tick():
    client, _ = create_client()

    received = []

    client.register_tick_callback(lambda tick: received.append(tick))

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000.0,
        volume=1000,
        timestamp=None,
    )

    client.emit_tick(tick)

    assert received[0].symbol == "NIFTY"
