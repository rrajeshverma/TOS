"""
Tests:
Live Candle -> Indicator Generation Flow

Flow:

BrokerTick
    |
    ▼
CandleBuilder
    |
    ▼
Candle
    |
    ▼
IndicatorEngine
    |
    ▼
IndicatorSet
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from engines.indicator_engine import IndicatorEngine
from market.candle_builder import CandleBuilder


def create_tick(price):
    return BrokerTick(
        symbol="NIFTY",
        ltp=price,
        volume=1000,
        timestamp=datetime.now(),
    )


def create_candle_series():
    builder = CandleBuilder()

    candles = []

    prices = [25000.0 + (index * 5) for index in range(40)]

    for price in prices:
        candle = builder.update(create_tick(price))

        candles.append(candle)

    return candles


def test_indicator_engine_accepts_live_candles():
    engine = IndicatorEngine()

    candles = create_candle_series()

    indicators = engine.calculate(candles)

    assert indicators is not None


def test_live_indicator_contains_ema():
    engine = IndicatorEngine()

    candles = create_candle_series()

    indicators = engine.calculate(candles)

    assert indicators.ema_high is not None


def test_live_indicator_contains_vwap():
    engine = IndicatorEngine()

    candles = create_candle_series()

    indicators = engine.calculate(candles)

    assert indicators.vwap is not None


def test_live_indicator_updates_after_new_candle():
    engine = IndicatorEngine()

    candles = create_candle_series()

    first = engine.calculate(candles)

    builder = CandleBuilder()

    candles = create_candle_series()

    first = engine.calculate(candles)

    candles.append(builder.update(create_tick(25200.0)))

    second = engine.calculate(candles)

    second = engine.calculate(candles)

    assert second is not None
    assert second != first
