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

from brokers.dhan.live_market_feed import LiveMarketFeed
from brokers.dhan.models import BrokerTick
from brokers.dhan.session import DhanSession


class WebSocketClient:
    """
    High-level websocket client used by MarketDataService.
    """

    def __init__(
        self,
        transport=None,
        session: DhanSession | None = None,
        live_market_feed: LiveMarketFeed | None = None,
    ) -> None:
        self.transport = transport
        self.session = session
        self.live_market_feed = live_market_feed

        self._connected = False
        self._subscriptions: set = set()
        self._tick_callback: Callable[[BrokerTick], None] | None = None

        if self.live_market_feed is not None:
            self.live_market_feed.register_tick_callback(
                self.emit_tick,
            )

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def subscriptions(self) -> set:
        return set(self._subscriptions)

    @property
    def tick_callback(self):
        return self._tick_callback

    def connect(self) -> None:
        """
        Connect websocket.
        """

        if self.live_market_feed is not None:
            self.live_market_feed.start()
            self._connected = True
            return

        #
        # Existing implementation
        #

        if self.session is not None:
            if not self.session.is_authenticated:
                raise RuntimeError(
                    "WebSocket requires authentication."
                )

            if self.transport is not None:
                self.transport.authenticate(
                    self.session.access_token,
                )

        if self.transport is not None:
            self.transport.connect()

        self._connected = True

    def disconnect(self) -> None:

        if self.live_market_feed is not None:
            self.live_market_feed.stop()
            self._connected = False
            return

        if self.transport is not None:
            self.transport.disconnect()

        self._connected = False

    def subscribe(
        self,
        instrument,
    ) -> None:
        """
        Subscribe instrument.
        """

        if self.live_market_feed is not None:
            self.live_market_feed.subscribe(
                [instrument],
            )
            self._subscriptions.add(instrument)
            return

        if self.session is not None and not self._connected:
            raise RuntimeError(
                "WebSocket is not connected."
            )

        if not self._connected:
            self._connected = True

        self._subscriptions.add(
            instrument,
        )

        if self.transport is not None:
            self.transport.subscribe(
                instrument,
            )

    def unsubscribe(
        self,
        instrument,
    ) -> None:

        self._subscriptions.discard(
            instrument,
        )

    def clear_subscriptions(self) -> None:
        self._subscriptions.clear()

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        self._tick_callback = callback

    def emit_tick(
        self,
        tick: BrokerTick,
    ) -> None:
        """
        Forward BrokerTick to MarketDataService.
        """

        if self._tick_callback is not None:
            self._tick_callback(
                tick,
            )

    def reset(self) -> None:
        self.disconnect()
        self._subscriptions.clear()
        self._tick_callback = None