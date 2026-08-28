"""
Dhan live market-feed adapter.
"""

from __future__ import annotations

import asyncio
import logging
import threading
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
        self._stop_event = threading.Event()
        self._callback: Callable[[BrokerTick], None] | None = None
        self._payload_logged = False

        self._instruments: set[tuple[int, str, int]] = set()

    def _on_connect(
        self,
        feed: MarketFeed,
    ) -> None:
        LOGGER.info(
            "Dhan market feed connected successfully | instruments=%s",
            feed.instruments,
        )

    def _on_close(
        self,
        _feed: MarketFeed,
        *args,
        **kwargs,
    ) -> None:
        LOGGER.warning(
            "Dhan SDK on_close | args=%s | kwargs=%s",
            args,
            kwargs,
        )


    def _on_error(
        self,
        _feed: MarketFeed,
        *args,
        **kwargs,
    ) -> None:
        LOGGER.error(
            "Dhan SDK on_error | args=%s | kwargs=%s",
            args,
            kwargs,
        )

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

        if data.get("type") != "Quote Data":
            return

        if not self._payload_logged:
            LOGGER.info(
                "Dhan first Quote Data payload: %s",
                data,
            )
            self._payload_logged = True

        LOGGER.info(
            "Dhan Quote Data | keys=%s | LTP=%s | LTT=%s | LTQ=%s | volume=%s",
            sorted(data.keys()),
            data.get("LTP"),
            data.get("LTT"),
            data.get("LTQ"),
            data.get("volume"),
        )

        tick = self._tick_mapper.to_broker_tick(data)

        if self._callback is not None:
            self._callback(tick)

    def _handle_sdk_tick(
        self,
        _feed: MarketFeed,
        data: dict,
    ) -> None:
        if not isinstance(data, dict):
            return

        self._on_tick(
            _feed,
            data,
        )

    def _run(self) -> None:
        reconnect_delay = 5
        max_reconnect_delay = 60

        LOGGER.info(
            "Dhan market feed thread started | instruments=%s",
            self._instruments,
        )

        try:
            while self._running and not self._stop_event.is_set():
                feed = None
                received_data = False

                try:
                    feed = MarketFeed(
                        dhan_context=self._context,
                        instruments=list(self._instruments),
                        version="v2",
                        on_connect=self._on_connect,
                        on_close=self._on_close,
                        on_error=self._on_error,
                    )

                    self._feed = feed

                    LOGGER.info("Connecting to Dhan market feed...")

                    # Connect once. Do NOT use feed.run(), because the
                    # Dhan SDK internally retries every second.
                    feed.run_forever()

                    LOGGER.info(
                        "Dhan market feed receive loop started."
                    )

                    reconnect_delay = 5

                    while (
                        self._running
                        and not self._stop_event.is_set()
                    ):
                        data = feed.loop.run_until_complete(
                            feed.get_instrument_data(),
                        )

                        if not isinstance(data, dict):
                            continue

                        received_data = True

                        self._handle_sdk_tick(
                            feed,
                            data,
                        )

                except ConnectionClosed as exc:
                    if self._running and not self._stop_event.is_set():
                        LOGGER.warning(
                            "Dhan market feed connection closed | "
                            "exception_type=%s | code=%s | reason=%s | "
                            "received_data=%s | reconnecting in %s seconds...",
                            type(exc).__name__,
                            getattr(exc, "code", None),
                            getattr(exc, "reason", None),
                            received_data,
                            reconnect_delay,
                        )

                        self._stop_event.wait(reconnect_delay)

                        reconnect_delay = min(
                            reconnect_delay * 2,
                            max_reconnect_delay,
                        )

                except Exception:
                    if not self._running or self._stop_event.is_set():
                        break

                    LOGGER.exception(
                        "Dhan market feed connection failed."
                    )

                    LOGGER.info(
                        "Retrying Dhan market feed connection in %s seconds...",
                        reconnect_delay,
                    )

                    self._stop_event.wait(reconnect_delay)

                    reconnect_delay = min(
                        reconnect_delay * 2,
                        max_reconnect_delay,
                    )

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

    def start(self) -> None:
        if self._running:
            return

        if not self._instruments:
            raise RuntimeError(
                "No instruments subscribed to Dhan market feed.",
            )

        self._stop_event.clear()
        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            name="dhan-market-feed",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        self._stop_event.set()

        feed = self._feed

        if feed is not None:
            try:
                loop = feed.loop

                if not loop.is_closed():
                    future = asyncio.run_coroutine_threadsafe(
                        feed.disconnect(),
                        loop,
                    )

                    try:
                        future.result(timeout=5)
                    except Exception:
                        pass
            except Exception:
                pass

        thread = self._thread

        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=5)

            if thread.is_alive():
                LOGGER.warning("Dhan market feed thread did not stop within timeout.")

        self._thread = None
        self._feed = None

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
