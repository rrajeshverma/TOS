from domain.candle import Candle


class MarketAdapter:
    def __init__(
        self,
        exchange="NSE",
    ):
        self.exchange = exchange

    def to_market_data(
        self,
        candle: Candle,
    ) -> dict:
        if candle is None:
            raise ValueError("Candle cannot be None")

        return {
            "symbol": candle.symbol,
            "exchange": self.exchange,
            "timeframe": candle.timeframe,
            "timestamp": candle.timestamp,
            "open": candle.open,
            "high": candle.high,
            "low": candle.low,
            "close": candle.close,
            "volume": candle.volume,
        }
