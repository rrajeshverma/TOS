from brokers.dhan.websocket import WebSocketClient


def test_websocket_initially_disconnected():
    ws = WebSocketClient()

    assert ws.is_connected is False


def test_connect_changes_state():
    ws = WebSocketClient()

    ws.connect()

    assert ws.is_connected is True


def test_disconnect_changes_state():
    ws = WebSocketClient()

    ws.connect()
    ws.disconnect()

    assert ws.is_connected is False


def test_multiple_connects_are_safe():
    ws = WebSocketClient()

    ws.connect()
    ws.connect()

    assert ws.is_connected is True


def test_multiple_disconnects_are_safe():
    ws = WebSocketClient()

    ws.disconnect()
    ws.disconnect()

    assert ws.is_connected is False


def test_connection_cycle():
    ws = WebSocketClient()

    ws.connect()
    ws.disconnect()
    ws.connect()

    assert ws.is_connected is True

def test_subscribe_adds_symbol():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")

    assert "NIFTY" in ws.subscriptions


def test_unsubscribe_removes_symbol():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")
    ws.unsubscribe("NIFTY")

    assert "NIFTY" not in ws.subscriptions


def test_duplicate_subscription_is_ignored():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")
    ws.subscribe("NIFTY")

    assert len(ws.subscriptions) == 1


def test_multiple_symbols():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")
    ws.subscribe("BANKNIFTY")
    ws.subscribe("FINNIFTY")

    assert len(ws.subscriptions) == 3


def test_unsubscribe_unknown_symbol_is_safe():
    ws = WebSocketClient()

    ws.unsubscribe("UNKNOWN")

    assert len(ws.subscriptions) == 0


def test_clear_all_subscriptions():
    ws = WebSocketClient()

    ws.subscribe("NIFTY")
    ws.subscribe("BANKNIFTY")

    ws.clear_subscriptions()

    assert ws.subscriptions == set()

def test_register_tick_callback():
    ws = WebSocketClient()

    def callback(tick):
        pass

    ws.register_tick_callback(callback)

    assert ws.tick_callback is callback


def test_emit_tick_invokes_callback():
    ws = WebSocketClient()

    received = []

    def callback(tick):
        received.append(tick)

    ws.register_tick_callback(callback)

    tick = {
        "symbol": "NIFTY",
        "ltp": 25100.50,
    }

    ws.emit_tick(tick)

    assert received == [tick]


def test_emit_without_callback_is_safe():
    ws = WebSocketClient()

    tick = {
        "symbol": "NIFTY",
        "ltp": 25100,
    }

    ws.emit_tick(tick)

from datetime import datetime

from brokers.dhan.models import BrokerTick


def test_emit_broker_tick():
    ws = WebSocketClient()

    received = []

    ws.register_tick_callback(received.append)

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000,
        volume=100,
        timestamp=datetime.now(),
    )

    ws.emit_tick(tick)

    assert received == [tick]

def test_reset_clears_state():
    ws = WebSocketClient()

    ws.connect()
    ws.subscribe("NIFTY")

    ws.reset()

    assert ws.is_connected is False
    assert ws.subscriptions == set()
    assert ws.tick_callback is None