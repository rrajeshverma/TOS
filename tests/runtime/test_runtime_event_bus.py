"""
Tests for TradingRuntime EventBus integration.
"""

from runtime.trading_runtime import TradingRuntime
from shared.event_bus import EventBus
from shared.events import Event


def test_runtime_has_event_bus() -> None:
    """Runtime owns an EventBus."""

    runtime = TradingRuntime({})

    assert isinstance(runtime.bus, EventBus)


def test_publish_forwards_event() -> None:
    """Runtime publishes events through the EventBus."""

    runtime = TradingRuntime({})

    received = []

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        received.append,
    )

    payload = {
        "market": "NIFTY",
        "history": [],
    }

    runtime.publish(
        Event.MARKET_TICK,
        payload,
    )

    assert received == [payload]


def test_multiple_subscribers_receive_runtime_event() -> None:
    """Multiple subscribers receive published runtime events."""

    runtime = TradingRuntime({})

    first = []
    second = []

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        first.append,
    )

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        second.append,
    )

    payload = {
        "price": 25100,
    }

    runtime.publish(
        Event.MARKET_TICK,
        payload,
    )

    assert first == [payload]
    assert second == [payload]


def test_publish_unknown_event() -> None:
    """Publishing an event without subscribers is safe."""

    runtime = TradingRuntime({})

    runtime.publish(
        Event.ORDER_FILLED,
        {
            "order_id": "123",
        },
    )


def test_runtime_bus_can_be_cleared() -> None:
    """EventBus remains reusable after clear()."""

    runtime = TradingRuntime({})

    received = []

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        received.append,
    )

    runtime.bus.clear()

    runtime.publish(
        Event.MARKET_TICK,
        100,
    )

    assert received == []
