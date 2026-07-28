"""
TOS Market Data Service

Orchestrates market data adapters and exposes
a unified interface to the trading system.
"""

from __future__ import annotations

from market.tick import Tick


class MarketDataService:
    """
    Unified market data service.
    """

    def __init__(
        self,
        adapter,
    ) -> None:

        if adapter is None:
            raise ValueError(
                "Market adapter is required"
            )

        self._adapter = adapter
        self._status = "STOPPED"


    def start(
        self,
    ) -> None:
        """
        Start market data service.
        """

        self._status = "RUNNING"


    def stop(
        self,
    ) -> None:
        """
        Stop market data service.
        """

        self._status = "STOPPED"


    def health(
        self,
    ) -> str:
        """
        Return service status.
        """

        return self._status


    def publish_tick(
        self,
        tick: Tick,
    ):
        """
        Publish tick through adapter.
        """

        return self._adapter.publish_tick(
            tick
        )


    def get_latest_tick(
        self,
        symbol: str,
    ):
        """
        Return latest tick.
        """

        last_tick = self._adapter.last_tick()

        if (
            last_tick
            and last_tick.symbol == symbol
        ):
            return last_tick

        return None
