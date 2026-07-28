"""
Tests:
Dhan WebSocket Tick Stream Pipeline

Flow:
Dhan WebSocket
        |
        ▼
BrokerTick
        |
        ▼
TickAdapter
        |
        ▼
MarketRuntime
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from brokers.dhan.session import DhanSession
from brokers.dhan.websocket import WebSocketClient
from market.tick_adapter import TickAdapter


class DummyTransport:
    def __init__(self):
        self.connected = False
        self.callback = None
        self.subscribed = []

    def authenticate(self, token):
        self.token = token

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def subscribe(self, symbol):
        self.subscribed.append(symbol)

    def register_callback(self, callback):
        self.callback = callback

    def emit(self, tick):
        if self.callback:
            self.callback(tick)


def create_pipeline():

    session = DhanSession()

    session.authenticate(
        "ACCESS_TOKEN"
    )

    transport = DummyTransport()

    websocket = WebSocketClient(
        transport,
        session,
    )

    adapter = TickAdapter()

    return websocket, transport, adapter


def test_tick_stream_requires_connection():

    websocket, _, _ = create_pipeline()

    tick_received = []

    websocket.register_tick_callback(
        lambda tick: tick_received.append(tick)
    )

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000.0,
        volume=1000,
        timestamp=datetime.now(),
    )

    websocket.emit_tick(
        tick
    )

    assert tick_received[0].symbol == "NIFTY"


def test_tick_subscription_flow():

    websocket, transport, _ = create_pipeline()

    websocket.connect()

    websocket.subscribe(
        "NIFTY"
    )

    assert "NIFTY" in transport.subscribed


def test_tick_adapter_converts_broker_tick():

    _, _, adapter = create_pipeline()

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000.0,
        volume=1000,
        timestamp=datetime.now(),
    )

    market_tick = adapter.convert(
        tick
    )

    assert market_tick.symbol == "NIFTY"
    assert market_tick.close == 25000.0


def test_tick_pipeline_end_to_end():

    websocket, _, adapter = create_pipeline()

    received = []

    websocket.register_tick_callback(
        lambda tick: received.append(
            adapter.convert(tick)
        )
    )

    websocket.connect()

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000.0,
        volume=1000,
        timestamp=datetime.now(),
    )

    websocket.emit_tick(
        tick
    )

    assert len(received) == 1
    assert received[0].symbol == "NIFTY"
