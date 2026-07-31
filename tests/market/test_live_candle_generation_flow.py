"""
Tests:
Live Tick -> Candle Generation Flow

Flow:

BrokerTick
    |
    ▼
TickAdapter
    |
    ▼
CandleBuilder
    |
    ▼
OHLC Candle
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from market.candle_builder import CandleBuilder


def create_tick(
    price=25000.0,
):
    return BrokerTick(
        symbol="NIFTY",
        ltp=price,
        volume=1000,
        timestamp=datetime.now(),
    )


def test_tick_can_create_candle():
    builder = CandleBuilder()

    tick = create_tick()

    candle = builder.update(tick)

    assert candle is not None
    assert candle.symbol == "NIFTY"


def test_multiple_ticks_update_candle():
    builder = CandleBuilder()

    ticks = [
        create_tick(25000.0),
        create_tick(25010.0),
        create_tick(24990.0),
    ]

    candle = None

    for tick in ticks:
        candle = builder.update(tick)

    assert candle.open == 25000.0
    assert candle.high == 25010.0
    assert candle.low == 24990.0
    assert candle.close == 24990.0


def test_candle_volume_accumulates():
    builder = CandleBuilder()

    tick1 = create_tick(25000.0)

    tick2 = create_tick(25005.0)

    builder.update(tick1)

    candle = builder.update(tick2)

    assert candle.volume > 0


def test_candle_generation_requires_tick():
    builder = CandleBuilder()

    try:
        builder.update(None)

    except ValueError:
        assert True

    else:
        assert False
