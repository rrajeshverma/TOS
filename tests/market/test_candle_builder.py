from datetime import datetime
from decimal import Decimal

from domain.market_tick import MarketTick
from market.candle_builder import CandleBuilder


def test_create_first_candle():
    builder = CandleBuilder(timeframe="5m")

    tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25000),
        volume=100,
        timestamp=datetime.now(),
    )

    candle = builder.update(tick)

    assert candle.open == Decimal(25000)
    assert candle.high == Decimal(25000)
    assert candle.low == Decimal(25000)
    assert candle.close == Decimal(25000)


def test_update_high_low_close():
    builder = CandleBuilder(timeframe="5m")

    t1 = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25000),
        volume=100,
        timestamp=datetime.now(),
    )

    t2 = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25050),
        volume=200,
        timestamp=datetime.now(),
    )

    builder.update(t1)

    candle = builder.update(t2)

    assert candle.high == Decimal(25050)
    assert candle.close == Decimal(25050)
