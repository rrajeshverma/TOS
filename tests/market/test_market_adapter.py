from datetime import datetime

from domain.candle import Candle
from market.market_adapter import MarketAdapter


def test_candle_to_market_payload():
    candle = Candle(
        symbol="NIFTY",
        timeframe="5m",
        timestamp=datetime.now(),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
    )

    adapter = MarketAdapter(exchange="NSE")

    payload = adapter.to_market_data(candle)

    assert payload["symbol"] == "NIFTY"
    assert payload["exchange"] == "NSE"
    assert payload["close"] == 105
