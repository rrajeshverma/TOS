"""
=========================================================
Trading Operating System (TOS)
Module      : Market Runtime
Version     : 1.1.0
Description : Coordinates live market data processing.
=========================================================
"""

from __future__ import annotations

from brokers.dhan.models import BrokerTick
from market.tick_adapter import TickAdapter


class MarketRuntime:
    """
    Coordinates live market data processing.

    Responsibilities:
    - Manage market runtime lifecycle
    - Receive broker ticks
    - Convert ticks into Market objects
    - Maintain latest market state
    """

    def __init__(
        self,
        feed=None,
    ) -> None:
        self.feed = feed
        self.running = False

        self.tick_adapter = TickAdapter()
        self._latest_market = None

    def start(self) -> None:
        """
        Start market runtime.
        """

        self.running = True

    def stop(self) -> None:
        """
        Stop market runtime.
        """

        self.running = False

    def is_running(self) -> bool:
        """
        Return runtime status.
        """

        return self.running

    def on_tick(
        self,
        tick: BrokerTick,
    ) -> None:
        """
        Receive broker tick.

        Tick is ignored when runtime is stopped.
        """

        if not self.running:
            return

        self._latest_market = self.tick_adapter.adapt(tick)

    def get_market(self):
        """
        Return latest converted Market object.
        """

        return self._latest_market
