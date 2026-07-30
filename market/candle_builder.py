from domain.market_tick import MarketTick
from domain.candle import Candle


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

    def update(
        self,
        tick: MarketTick,
    ) -> Candle:
        if tick is None:
            raise ValueError("Tick cannot be None.")

        existing = self._candles.get(tick.symbol)

        if existing is None:
            candle = Candle(
                symbol=tick.symbol,
                timeframe=self.timeframe,
                timestamp=tick.timestamp,
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
                timestamp=tick.timestamp,
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

        self._candles[tick.symbol] = candle

        return candle
