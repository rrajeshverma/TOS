"""
Tests:
Live Candle -> Indicator -> Decision Signal Flow

Flow:

BrokerTick
    |
    ▼
CandleBuilder
    |
    ▼
IndicatorEngine
    |
    ▼
DecisionEngine
    |
    ▼
Decision
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.indicator_engine import IndicatorEngine
from market.candle_builder import CandleBuilder


def create_tick(price: float):

    return BrokerTick(
        symbol="NIFTY",
        ltp=price,
        volume=1000,
        timestamp=datetime.now(),
    )


def create_live_market():

    builder = CandleBuilder()

    candles = []

    prices = [
        25000 + (index * 10)
        for index in range(40)
    ]

    for price in prices:
        candles.append(
            builder.update(
                create_tick(price)
            )
        )

    latest = candles[-1]

    return Market(
        symbol=latest.symbol,
        exchange="NSE",
        timeframe="TICK",
        open=latest.open,
        high=latest.high,
        low=latest.low,
        close=latest.close,
        volume=latest.volume,
        timestamp=latest.timestamp,
    ), candles


def test_live_market_generates_indicators():

    _, candles = create_live_market()

    engine = IndicatorEngine()

    indicators = engine.calculate(
        candles
    )

    assert indicators is not None
    assert indicators.ema_high is not None
    assert indicators.vwap is not None


def test_decision_engine_accepts_live_signal():

    market, candles = create_live_market()

    indicator_engine = IndicatorEngine()

    indicators = indicator_engine.calculate(
        candles
    )

    decision_engine = DecisionEngine()

    decision = decision_engine.evaluate(
        market,
        indicators,
    )

    assert decision is not None


def test_live_signal_flow_returns_valid_status():

    market, candles = create_live_market()

    indicators = IndicatorEngine().calculate(
        candles
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    assert decision.status is not None


def test_no_signal_is_valid_market_state():

    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="TICK",
        open=25000,
        high=25000,
        low=25000,
        close=25000,
        volume=1000,
        timestamp=datetime.now(),
    )

    indicators = IndicatorSet(
        ema_high=25010,
        ema_low=24990,
        vwap=25000,
        rsi=50,
        volume_average=1000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    assert decision is not None
