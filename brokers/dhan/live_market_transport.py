"""
Live Market Transport.

Transport implementation backed by the official
Dhan MarketFeed SDK.
"""

from __future__ import annotations

from brokers.dhan.live_market_feed import LiveMarketFeed


class LiveMarketTransport:
    """
    Transport adapter for the official Dhan MarketFeed.
    """

    def __init__(
        self,
        market_feed: LiveMarketFeed,
    ) -> None:
        self._market_feed = market_feed

    def connect(self) -> None:
        """
        Connect to Dhan MarketFeed.
        """
        self._market_feed.start()

    def disconnect(self) -> None:
        """
        Disconnect from Dhan MarketFeed.
        """
        self._market_feed.stop()

    def authenticate(
        self,
        access_token: str,
    ) -> None:
        """
        Authentication is handled internally by
        MarketFeed through DhanContext.
        """
        return

    def subscribe(
        self,
        instruments: list[tuple],
    ) -> None:
        """
        Subscribe to instruments.
        """
        self._market_feed.subscribe(
            instruments,
        )

    def unsubscribe(
        self,
        instruments: list[tuple],
    ) -> None:
        """
        Unsubscribe instruments.
        """
        self._market_feed._market_feed.unsubscribe_symbols(
            instruments,
        )
