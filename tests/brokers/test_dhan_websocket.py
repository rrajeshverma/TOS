"""
Tests for Dhan WebSocket client abstraction.
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from brokers.dhan.websocket import WebSocketClient


def create_tick():
    return BrokerTick(
        symbol="NIFTY",
        ltp=22500.0,
        volume=100000,
        timestamp=datetime.now(),
    )


def test_initial_state():
    ws = WebSocketClient()

    assert ws.is_connected is False
    assert ws.subscriptions == set()


def test_connect():
    ws = WebSocketClient()

    ws.connect()

    assert ws.is_connected is True


def test_disconnect():
    ws = WebSocketClient()

    ws.connect()
    ws.disconnect()

    assert ws.is_connected is False


def test_subscribe_symbol():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")

    assert "NIFTY" in ws.subscriptions


def test_unsubscribe_symbol():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")
    ws.unsubscribe("NIFTY")

    assert "NIFTY" not in ws.subscriptions


def test_tick_callback():
    ws = WebSocketClient()

    received = []

    def callback(tick):
        received.append(tick)

    ws.register_tick_callback(callback)

    tick = create_tick()

    ws.emit_tick(tick)

    assert received[0] == tick


def test_emit_without_callback():
    ws = WebSocketClient()

    ws.emit_tick(create_tick())


def test_reset():
    ws = WebSocketClient()

    ws.connect()
    ws.subscribe("NIFTY")

    ws.reset()

    assert ws.is_connected is False
    assert ws.subscriptions == set()
    assert ws.tick_callback is None
