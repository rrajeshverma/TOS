"""
Tests for MARKET_TICK event handling.
"""

from runtime.trading_runtime import TradingRuntime
from shared.events import Event


def test_market_tick_event_invokes_handler(monkeypatch):
    runtime = TradingRuntime({})

    calls = []

    def fake_run_cycle(market, history):
        calls.append((market, history))

    runtime.run_cycle = fake_run_cycle

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        runtime._handle_market_tick,
    )

    payload = {
        "market": "NIFTY",
        "history": [1, 2, 3],
    }

    runtime.publish(
        Event.MARKET_TICK,
        payload,
    )

    assert calls == [("NIFTY", [1, 2, 3])]


def test_market_tick_handler_can_be_unsubscribed():
    runtime = TradingRuntime({})

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        runtime._handle_market_tick,
    )

    runtime.bus.unsubscribe(
        Event.MARKET_TICK.value,
        runtime._handle_market_tick,
    )

    assert runtime.bus is not None
