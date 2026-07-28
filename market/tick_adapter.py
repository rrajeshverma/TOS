"""
Market Tick Adapter

Converts broker ticks into TOS Market objects.
"""

from __future__ import annotations

from domain.market import Market


class TickAdapter:
    """
    Converts broker ticks into Market domain objects.
    """

    def __init__(self) -> None:
        self._ticks: dict[str, object] = {}

    def adapt(
        self,
        tick,
    ) -> Market:
        """
        Convert BrokerTick to Market object.
        """

        if tick is None:
            raise ValueError(
                "Tick cannot be None."
            )

        market = Market(
                symbol=tick.symbol,
                exchange="NSE",
                timeframe="TICK",
                open=tick.ltp,
                high=tick.ltp,
                low=tick.ltp,
                close=tick.ltp,
                volume=tick.volume,
                timestamp=tick.timestamp,
        )

        self._ticks[
            tick.symbol
        ] = tick

        return market

    def convert(
        self,
        tick,
    ) -> Market:
        """
        New pipeline alias.
        """

        return self.adapt(
            tick
        )

    def last_tick(
        self,
        symbol: str,
    ):
        """
        Return latest market tick.
        """

        return self._ticks.get(
            symbol
        )

    def clear(self) -> None:
        """
        Clear all ticks.
        """

        self._ticks.clear()

    def clear_ticks(self) -> None:
        """
        Backward-compatible alias.
        """

        self.clear()