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

from dhanhq import MarketFeed

from brokers.dhan.live_market_feed import LiveMarketFeed
from brokers.dhan.models import BrokerTick
from brokers.dhan.session import DhanSession
from domain.instrument import Instrument


class WebSocketClient:
    """High-level websocket client used by MarketDataService."""

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

    @staticmethod
    def _to_dhan_subscription(
        instrument: Instrument,
    ) -> tuple[int, str, int]:
        exchange_map = {
            "IDX_I": 0,
            "NSE_EQ": 1,
            "NSE_FNO": 2,
            "NSE_CURRENCY": 3,
            "BSE_EQ": 4,
            "MCX_COMM": 5,
            "BSE_CURRENCY": 7,
            "BSE_FNO": 8,
        }

        try:
            exchange = exchange_map[instrument.exchange_segment]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported Dhan exchange segment: {instrument.exchange_segment}",
            ) from exc

        return (
            exchange,
            str(instrument.security_id),
            MarketFeed.Ticker,
        )

    def connect(self) -> None:
        """Connect websocket."""

        if self.live_market_feed is not None:
            self.live_market_feed.start()
            self._connected = True
            return

        if self.session is not None:
            if not self.session.is_authenticated:
                raise RuntimeError(
                    "WebSocket requires authentication.",
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
        """Subscribe an instrument."""

        if self.live_market_feed is not None:
            if not isinstance(instrument, Instrument):
                raise TypeError(
                    "Dhan live feed subscriptions require an Instrument.",
                )

            dhan_instrument = self._to_dhan_subscription(
                instrument,
            )

            self.live_market_feed.subscribe(
                [dhan_instrument],
            )

            self._subscriptions.add(
                instrument.symbol,
            )
            return

        if self.session is not None and not self._connected:
            raise RuntimeError(
                "WebSocket is not connected.",
            )

        if not self._connected:
            self._connected = True

        self._subscriptions.add(instrument)

        if self.transport is not None:
            self.transport.subscribe(instrument)

    def unsubscribe(
        self,
        instrument,
    ) -> None:
        self._subscriptions.discard(
            instrument.symbol if isinstance(instrument, Instrument) else instrument,
        )

        if self.live_market_feed is not None:
            if not isinstance(instrument, Instrument):
                raise TypeError(
                    "Dhan live feed subscriptions require an Instrument.",
                )

            self.live_market_feed.unsubscribe(
                [self._to_dhan_subscription(instrument)],
            )

    def clear_subscriptions(self) -> None:
        self._subscriptions.clear()

        if self.live_market_feed is not None:
            self.live_market_feed.unsubscribe(
                list(self.live_market_feed.instruments),
            )

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        self._tick_callback = callback

    def emit_tick(
        self,
        tick: BrokerTick,
    ) -> None:
        """Forward BrokerTick to MarketDataService."""

        if self._tick_callback is not None:
            self._tick_callback(tick)

    def reset(self) -> None:
        self.disconnect()
        self._subscriptions.clear()
        self._tick_callback = None
