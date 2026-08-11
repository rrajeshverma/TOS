from datetime import datetime

from domain.candle import Candle
from domain.market_tick import MarketTick


class CandleBuilder:
    """
    Builds OHLC candles from live ticks.
    """

    def __init__(
        self,
        timeframe: str = "5m",
    ):
        self.timeframe = timeframe
        self._candles = {}

    def _bucket_timestamp(
        self,
        timestamp: datetime,
    ) -> datetime:
        if self.timeframe.endswith("m"):
            minutes = int(self.timeframe[:-1])

            bucket_minute = (timestamp.minute // minutes) * minutes

            return timestamp.replace(
                minute=bucket_minute,
                second=0,
                microsecond=0,
            )

        raise ValueError(f"Unsupported timeframe: {self.timeframe}")

    def update(
        self,
        tick: MarketTick,
    ) -> Candle:
        if tick is None:
            raise ValueError("Tick cannot be None.")

        if tick.timestamp is None:
            raise ValueError("Tick timestamp cannot be None.")

        bucket = self._bucket_timestamp(
            tick.timestamp,
        )

        key = (
            tick.symbol,
            bucket,
        )

        existing = self._candles.get(key)

        if existing is None:
            candle = Candle(
                symbol=tick.symbol,
                timeframe=self.timeframe,
                timestamp=bucket,
                open=tick.ltp,
                high=tick.ltp,
                low=tick.ltp,
                close=tick.ltp,
                volume=tick.volume,
            )

        else:
            candle = Candle(
                symbol=existing.symbol,
                timeframe=existing.timeframe,
                timestamp=existing.timestamp,
                open=existing.open,
                high=max(
                    existing.high,
                    tick.ltp,
                ),
                low=min(
                    existing.low,
                    tick.ltp,
                ),
                close=tick.ltp,
                volume=(existing.volume + tick.volume),
            )

        self._candles[key] = candle

        return candle
