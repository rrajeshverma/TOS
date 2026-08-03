"""
Live Dhan Market Feed.

Thin wrapper around the official Dhan MarketFeed SDK.
Responsible only for receiving live market data and
converting it into BrokerTick objects.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
import logging

from dhanhq import MarketFeed

from brokers.dhan.models import BrokerTick

LOGGER = logging.getLogger(__name__)


class LiveMarketFeed:
    """
    Thin wrapper around the official Dhan MarketFeed.
    """

    def __init__(
        self,
        dhan_context,
        instruments: list[tuple],
    ) -> None:
        self._tick_callback: Callable[[BrokerTick], None] | None = None

        self._market_feed = MarketFeed(
            dhan_context=dhan_context,
            instruments=instruments,
            version="v2",
            on_connect=self._on_connect,
            on_close=self._on_close,
            on_error=self._on_error,
            on_ticks=self._on_ticks,
        )

    def start(self) -> None:
        """
        Start live market feed.
        """
        self._market_feed.start()

    def stop(self) -> None:
        """
        Stop live market feed.
        """
        self._market_feed.close_connection()

    def subscribe(
        self,
        instruments: list[tuple],
    ) -> None:
        """
        Subscribe additional instruments.
        """
        self._market_feed.subscribe_symbols(
            instruments,
        )

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        """
        Register BrokerTick callback.
        """
        self._tick_callback = callback

    # ----------------------------------------------------
    # SDK Callbacks
    # ----------------------------------------------------

    def _on_connect(
        self,
        feed,
    ) -> None:
        LOGGER.info("Connected to Dhan MarketFeed.")

    def _on_close(
        self,
        feed,
    ) -> None:
        LOGGER.info("Disconnected from Dhan MarketFeed.")

    def _on_error(
        self,
        feed,
        error,
    ) -> None:
        LOGGER.exception(
            "MarketFeed error: %s",
            error,
        )

    def _on_ticks(
        self,
        feed,
        data: dict,
    ) -> None:
        """
        Convert Dhan market data into BrokerTick.
        """

        if self._tick_callback is None:
            return

        broker_tick = BrokerTick(
            symbol=str(data.get("security_id", "")),
            ltp=Decimal(data.get("LTP", "0")),
            volume=int(data.get("volume", 0)),
            timestamp=datetime.now(),
        )

        self._tick_callback(
            broker_tick,
        )
