"""
TOS Paper Market Data Adapter

Provides simulated market data using the same
event model as live market feeds.
"""

from __future__ import annotations

from market.event import MarketEvent
from market.tick import Tick


class PaperMarketAdapter:
    """
    Paper trading market data source.
    """

    def __init__(self) -> None:
        self._last_tick: Tick | None = None

    def publish_tick(
        self,
        tick: Tick,
    ) -> MarketEvent:
        """
        Convert tick into market event.
        """

        if tick is None:
            raise ValueError("Tick cannot be None")

        if not isinstance(
            tick,
            Tick,
        ):
            raise ValueError("Invalid tick")

        self._last_tick = tick

        return MarketEvent(
            event_type="PRICE_UPDATE",
            tick=tick,
            source="PAPER",
        )

    def last_tick(
        self,
    ) -> Tick | None:
        """
        Return latest published tick.
        """

        return self._last_tick
