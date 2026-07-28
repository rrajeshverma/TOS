"""
TOS Market Data Health Monitor

Tracks market feed freshness and recovery requirements.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from market.tick import Tick


class MarketDataHealth:
    """
    Market data health tracker.
    """

    STALE_THRESHOLD = timedelta(
        minutes=5
    )

    def __init__(self) -> None:

        self._last_tick_time: datetime | None = None


    def record_tick(
        self,
        tick: Tick,
    ) -> None:
        """
        Record latest market tick.
        """

        if tick is None:
            raise ValueError(
                "Tick cannot be None"
            )

        self._last_tick_time = (
            tick.timestamp
        )


    def last_tick_time(
        self,
    ) -> datetime | None:
        """
        Return latest tick timestamp.
        """

        return self._last_tick_time


    def is_healthy(
        self,
    ) -> bool:
        """
        Check market data availability.
        """

        if self._last_tick_time is None:
            return False

        return not self.is_feed_stale()


    def is_feed_stale(
        self,
    ) -> bool:
        """
        Detect stale market feed.
        """

        if self._last_tick_time is None:
            return True

        return (
            datetime.now()
            - self._last_tick_time
            > self.STALE_THRESHOLD
        )


    def recovery_required(
        self,
    ) -> bool:
        """
        Determine if feed recovery is needed.
        """

        return not self.is_healthy()
