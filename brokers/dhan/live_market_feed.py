from __future__ import annotations

import random
import logging
from datetime import datetime
from decimal import Decimal
from collections.abc import Callable

from brokers.dhan.models import BrokerTick

LOGGER = logging.getLogger(__name__)


class LiveMarketFeed:
    """
    Mock Market Feed (Temporary replacement for Dhan WebSocket)
    """

    def __init__(self) -> None:
        self._tick_callback: Callable[[BrokerTick], None] | None = None

    # ----------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------

    def start(self) -> None:
        LOGGER.info("Mock Market Feed started.")

    def stop(self) -> None:
        LOGGER.info("Mock Market Feed stopped.")

    def subscribe(self, instruments: list[tuple]) -> None:
        LOGGER.info("Subscribed (mock): %s", instruments)

    def register_tick_callback(
        self,
        callback: Callable[[BrokerTick], None],
    ) -> None:
        self._tick_callback = callback

    # ----------------------------------------------------
    # MOCK TICK GENERATOR
    # ----------------------------------------------------

    def generate_tick(self) -> None:
        """
        Call this manually or from loop to simulate ticks
        """
        if self._tick_callback is None:
            return

        price = 22000 + random.randint(-50, 50)

        tick = BrokerTick(
            symbol="NIFTY",
            ltp=Decimal(str(price)),
            volume=100,
            timestamp=datetime.now(),
        )

        self._tick_callback(tick)
