"""
WebSocket client abstraction for Dhan Broker.

Manages connection state, subscriptions, and tick callbacks.
Actual Dhan WebSocket integration will be added later.
"""

from __future__ import annotations

from collections.abc import Callable

from brokers.dhan.models import BrokerTick


class WebSocketClient:
    """Represents the broker WebSocket client."""

    def __init__(self) -> None:
        self._connected = False
        self._subscriptions: set[str] = set()
        self._tick_callback: Callable[[BrokerTick], None] | None = None

    @property
    def is_connected(self) -> bool:
        """Return the connection state."""
        return self._connected

    @property
    def subscriptions(self) -> set[str]:
        """Return a copy of the subscribed symbols."""
        return set(self._subscriptions)

    @property
    def tick_callback(self) -> Callable[[BrokerTick], None] | None:
        """Return the registered tick callback."""
        return self._tick_callback

    def connect(self) -> None:
        """Connect the client."""
        self._connected = True

    def disconnect(self) -> None:
        """Disconnect the client."""
        self._connected = False

    def subscribe(self, symbol: str) -> None:
        """Subscribe to a symbol."""
        self._subscriptions.add(symbol)

    def unsubscribe(self, symbol: str) -> None:
        """Unsubscribe from a symbol."""
        self._subscriptions.discard(symbol)

    def clear_subscriptions(self) -> None:
        """Remove all subscriptions."""
        self._subscriptions.clear()

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        """Register a callback for incoming ticks."""
        self._tick_callback = callback

    def emit_tick(self, tick: BrokerTick) -> None:
        """Emit a tick to the registered callback."""
        if self._tick_callback is not None:
            self._tick_callback(tick)

    def reset(self) -> None:
        """Reset the client state."""
        self.disconnect()
        self.clear_subscriptions()
        self._tick_callback = None
