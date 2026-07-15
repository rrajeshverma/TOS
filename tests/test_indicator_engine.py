from datetime import datetime, timedelta

from domain.market import Market
from domain.indicator_set import IndicatorSet
from engines.indicator_engine import IndicatorEngine


def create_market(price: float, volume: int, ts: datetime) -> Market:
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=ts,
        open=price - 1,
        high=price + 1,
        low=price - 2,
        close=price,
        volume=volume,
    )


def test_indicator_engine_returns_indicator_set():
    engine = IndicatorEngine()

    start = datetime(2026, 1, 1, 9, 15)

    candles = []

    for i in range(40):
        candles.append(
            create_market(
                price=24000 + i,
                volume=100000 + (i * 100),
                ts=start + timedelta(minutes=5 * i),
            )
        )

    indicator = engine.calculate(candles)

    assert isinstance(indicator, IndicatorSet)

    assert indicator.ema_high > 0
    assert indicator.ema_low > 0
    assert indicator.vwap > 0
    assert indicator.rsi >= 0
    assert indicator.volume_average > 0