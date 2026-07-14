from datetime import datetime

from domain.market import Market


market = Market(
    symbol="NIFTY",
    exchange="NSE",
    timeframe="5m",
    timestamp=datetime.now(),
    open=24100,
    high=24125,
    low=24095,
    close=24120,
    volume=152340
)

print(market)

print(market.is_bullish)

print(market.body_size)

print(market.candle_range)