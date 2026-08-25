"""
Dhan live market-feed adapter.
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections.abc import Callable

from dhanhq import DhanContext, MarketFeed
from websockets.exceptions import ConnectionClosed

from brokers.dhan.models import BrokerTick
from brokers.dhan.tick_mapper import DhanTickMapper
from brokers.instrument_mapper import InstrumentMapper

LOGGER = logging.getLogger("brokers.dhan.live_market_feed")


class LiveMarketFeed:
    """Dhan live market-feed adapter."""

    def __init__(
        self,
        client_id: str,
        access_token: str,
        instrument_mapper: InstrumentMapper,
    ) -> None:
        self._context = DhanContext(
            client_id,
            access_token,
        )
        self._tick_mapper = DhanTickMapper(
            instrument_mapper,
        )

        self._feed: MarketFeed | None = None
        self._thread: threading.Thread | None = None
        self._running = False
        self._callback: Callable[[BrokerTick], None] | None = None

        self._instruments: set[tuple[int, str, int]] = set()

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def instruments(self) -> set[tuple[int, str, int]]:
        return set(self._instruments)

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        self._callback = callback

    def _on_tick(
        self,
        _feed: MarketFeed,
        data: dict,
    ) -> None:
        if not isinstance(data, dict):
            return

        if data.get("type") != "Ticker Data":
            return

        tick = self._tick_mapper.to_broker_tick(data)

        if self._callback is not None:
            self._callback(tick)

    def _run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        LOGGER.info(
            "Dhan market feed thread started | instruments=%s",
            self._instruments,
        )

        try:
            while self._running:
                feed = None

                try:
                    feed = MarketFeed(
                        dhan_context=self._context,
                        instruments=list(self._instruments),
                        version="v2",
                    )

                    self._feed = feed

                    LOGGER.info("Connecting to Dhan market feed...")

                    feed.run_forever()

                    LOGGER.info("Dhan market feed connected successfully.")

                    while self._running:
                        data = feed.get_data()

                        if data is not None:
                            LOGGER.debug(
                                "Dhan market data received: %s",
                                data.get("type"),
                            )

                            self._on_tick(
                                feed,
                                data,
                            )

                except ConnectionClosed:
                    if self._running:
                        LOGGER.warning(
                            "Dhan market feed connection closed. Reconnecting in 5 seconds..."
                        )
                        time.sleep(5)

                except Exception:
                    LOGGER.exception("Dhan market feed connection failed.")

                    if self._running:
                        LOGGER.info("Retrying Dhan market feed connection in 5 seconds...")
                        time.sleep(5)

                finally:
                    self._feed = None

                    if feed is not None:
                        try:
                            if not feed.loop.is_closed():
                                feed.loop.run_until_complete(
                                    feed.disconnect(),
                                )
                        except Exception:
                            pass

        finally:
            LOGGER.info("Dhan market feed thread stopping.")

            self._running = False

            try:
                if not loop.is_closed():
                    loop.close()
            except Exception:
                pass

    def start(self) -> None:
        if self._running:
            return

        if not self._instruments:
            raise RuntimeError(
                "No instruments subscribed to Dhan market feed.",
            )

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            name="dhan-market-feed",
        )
        self._thread.start()

    def stop(self) -> None:
        self._running = False

        thread = self._thread

        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=5)

        self._thread = None

    def subscribe(
        self,
        instruments: list[tuple[int, str, int]],
    ) -> None:
        new_instruments = set(instruments)
        self._instruments.update(new_instruments)

        if self._feed is not None:
            self._feed.subscribe_symbols(
                list(new_instruments),
            )

    def unsubscribe(
        self,
        instruments: list[tuple[int, str, int]],
    ) -> None:
        removed = set(instruments)
        self._instruments.difference_update(removed)

        if self._feed is not None:
            self._feed.unsubscribe_symbols(
                list(removed),
            )
