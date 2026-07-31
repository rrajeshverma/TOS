"""
Trading integration pipeline.

Receives live broker ticks, builds Market history and forwards
completed market updates to TradingRuntime.
"""

from __future__ import annotations

from collections import defaultdict

from domain.market_tick import MarketTick


class TradingPipeline:
    MAX_HISTORY = 500

    def __init__(
        self,
        candle_builder,
        market_engine,
        indicator_engine,
        runtime,
        exchange: str = "NSE",
    ) -> None:
        self._candle_builder = candle_builder
        self._market_engine = market_engine
        self._indicator_engine = indicator_engine
        self._runtime = runtime
        self._exchange = exchange

        self._history: dict[str, list] = defaultdict(list)

    def on_tick(self, tick: MarketTick):
        candle = self._candle_builder.update(tick)

        if candle is None:
            return None

        market = self._market_engine.build_market(
            {
                "symbol": candle.symbol,
                "exchange": self._exchange,
                "timeframe": candle.timeframe,
                "timestamp": candle.timestamp,
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
                "volume": candle.volume,
            }
        )

        history = self._history[market.symbol]
        history.append(market)

        if len(history) > self.MAX_HISTORY:
            history.pop(0)

        if len(history) < self._indicator_engine.MIN_CANDLES:
            return None

        return self._runtime.on_market_tick(
            market,
            history,
        )
