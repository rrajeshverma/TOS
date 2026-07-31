"""
TOS Market Data Stream

Broker-independent market event stream.
"""

from __future__ import annotations

from market.event import MarketEvent


class MarketStream:
    """
    Maintains market subscriptions and latest ticks.
    """

    def __init__(self) -> None:
        self._subscriptions: set[str] = set()
        self._ticks: dict[str, object] = {}

    def subscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Subscribe to market symbol.
        """

        if not symbol:
            raise ValueError("Symbol is required")

        self._subscriptions.add(symbol)

    def unsubscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Remove symbol subscription.
        """

        self._subscriptions.discard(symbol)

    def subscriptions(
        self,
    ) -> set[str]:
        """
        Return active subscriptions.
        """

        return set(self._subscriptions)

    def publish(
        self,
        event: MarketEvent,
    ) -> None:
        """
        Publish market event.
        """

        if event is None:
            raise ValueError("Market event cannot be None")

        self._ticks[event.tick.symbol] = event.tick

    def latest_tick(
        self,
        symbol: str,
    ):
        """
        Return latest tick for symbol.
        """

        return self._ticks.get(symbol)
