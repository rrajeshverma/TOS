"""
Dhan WebSocket Client

Handles:
- Authentication
- Connection lifecycle
- Subscriptions
- Tick callbacks
"""

from __future__ import annotations

from collections.abc import Callable

from brokers.dhan.models import BrokerTick
from brokers.dhan.session import DhanSession


class WebSocketClient:
    """
    Dhan websocket client abstraction.
    """

    def __init__(
        self,
        transport=None,
        session: DhanSession | None = None,
    ) -> None:

        self.transport = transport

        self.session = session

        self._connected = False
        self._subscriptions: set[str] = set()
        self._tick_callback: Callable[
            [BrokerTick],
            None,
        ] | None = None

    @property
    def is_connected(self) -> bool:
        """
        Return connection state.
        """

        return self._connected

    @property
    def subscriptions(self) -> set[str]:
        """
        Return subscribed symbols.
        """

        return set(self._subscriptions)

    @property
    def tick_callback(self):
        """
        Return tick callback.
        """

        return self._tick_callback

    def connect(self) -> None:
        """
        Connect websocket.

        Authentication is required only when
        a DhanSession is supplied.
        """

        if self.session is not None:

            if not self.session.is_authenticated:
                raise RuntimeError(
                    "WebSocket requires authentication."
                )

            if self.transport is not None:
                self.transport.authenticate(
                    self.session.access_token
                )

        if self.transport is not None:
            self.transport.connect()

        self._connected = True

    def disconnect(self) -> None:
        """
        Disconnect websocket.
        """

        if self.transport is not None:
            self.transport.disconnect()

        self._connected = False

    def subscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Subscribe symbol.

        In authenticated Dhan mode,
        websocket must be connected first.
        """

        if self.session is not None and not self._connected:
            raise RuntimeError(
                "WebSocket is not connected."
            )

        if not self._connected:
            self._connected = True

        self._subscriptions.add(symbol)

        if self.transport is not None:
            self.transport.subscribe(
                symbol
            )

    def unsubscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Remove subscription.
        """

        self._subscriptions.discard(symbol)

    def clear_subscriptions(self) -> None:
        """
        Remove all subscribed symbols.
        """

        self._subscriptions.clear()

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        """
        Register tick callback.
        """

        self._tick_callback = callback

    def emit_tick(
        self,
        tick: BrokerTick,
    ) -> None:
        """
        Emit received tick.
        """

        if self._tick_callback is not None:
            self._tick_callback(tick)

    def reset(self) -> None:
        """
        Reset websocket state.
        """

        self.disconnect()
        self._subscriptions.clear()
        self._tick_callback = None