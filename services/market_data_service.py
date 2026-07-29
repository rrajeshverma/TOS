"""
Market Data Service

Coordinates market data subscriptions and tick delivery.
"""

from __future__ import annotations

from collections.abc import Callable

from brokers.dhan.models import BrokerTick
from brokers.dhan.websocket import WebSocketClient

from domain.market_tick import MarketTick

from decimal import Decimal

class MarketDataService:
    """
    High-level market data service.
    """

    def __init__(
        self,
        websocket: WebSocketClient,
    ) -> None:
        self.websocket = websocket

    def connect(self) -> None:
        """
        Connect market data feed.
        """
        self.websocket.connect()

    def disconnect(self) -> None:
        """
        Disconnect market data feed.
        """
        self.websocket.disconnect()

    def subscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Subscribe to market data.
        """
        self.websocket.subscribe(symbol)

    def unsubscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Unsubscribe from market data.
        """
        self.websocket.unsubscribe(symbol)

    def clear_subscriptions(self) -> None:
        """
        Remove all subscriptions.
        """
        self.websocket.clear_subscriptions()

    def register_tick_handler(
        self,
        handler: Callable[[BrokerTick], None],
    ) -> None:
        """
        Register tick callback.
        """
        self.websocket.register_tick_callback(handler)

    @property
    def is_connected(self) -> bool:
        """
        Current websocket connection state.
        """
        return self.websocket.is_connected

    @property
    def subscriptions(self) -> set[str]:
        """
        Current subscriptions.
        """
        return self.websocket.subscriptions

    def to_market_tick(
        self,
        broker_tick: BrokerTick,
    ) -> MarketTick:
        """
        Convert broker tick into domain tick.
        """

        return MarketTick(
            symbol=broker_tick.symbol,
            ltp=Decimal(str(broker_tick.ltp)),
            volume=broker_tick.volume,
            timestamp=broker_tick.timestamp,
        )

    def emit_market_tick(
        self,
        broker_tick: BrokerTick,
    ) -> None:
        """
        Convert broker tick into domain tick and
        forward to registered handler.
        """

        market_tick = self.to_market_tick(broker_tick)

        if self.websocket.tick_callback is not None:
            self.websocket.tick_callback(market_tick)