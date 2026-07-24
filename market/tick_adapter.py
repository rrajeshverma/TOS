"""
=========================================================
Trading Operating System (TOS)
Module      : Tick Adapter
Version     : 1.0.0
Description : Converts broker ticks into market runtime format.
=========================================================
"""

from __future__ import annotations

from brokers.dhan.models import BrokerTick
from domain.market import Market


class TickAdapter:
    """
    Converts broker market ticks into TOS Market objects.
    """

    def __init__(self) -> None:
        self._last_ticks: dict[str, BrokerTick] = {}

    def adapt(
        self,
        tick: BrokerTick,
    ) -> Market:
        """
        Convert BrokerTick into Market candle object.

        For real candle aggregation, this will later
        connect with MarketRuntime.
        """

        if tick is None:
            raise ValueError(
                "tick cannot be None"
            )

        self._last_ticks[tick.symbol] = tick

        return Market(
            symbol=tick.symbol,
            exchange="NSE",
            timeframe="TICK",
            timestamp=tick.timestamp,
            open=tick.ltp,
            high=tick.ltp,
            low=tick.ltp,
            close=tick.ltp,
            volume=tick.volume,
        )

    def last_tick(
        self,
        symbol: str,
    ) -> BrokerTick | None:
        """
        Return latest tick for symbol.
        """

        return self._last_ticks.get(symbol)

    def clear(self) -> None:
        """
        Clear cached ticks.
        """

        self._last_ticks.clear()
