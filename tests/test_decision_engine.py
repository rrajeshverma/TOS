from datetime import datetime

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from shared.enums import DecisionStatus, Signal


def create_market(close: float) -> Market:
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime(2026, 8, 18, 11, 0),
        open=close - 5,
        high=close + 10,
        low=close - 10,
        close=close,
        volume=100000,
    )


def test_buy_ce_signal():
    engine = DecisionEngine()

    market = create_market(25000)

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    decision = engine.evaluate(market, indicators)

    assert decision.signal == Signal.BUY_CE
    assert decision.status == DecisionStatus.VALID
    assert decision.is_tradeable


def test_buy_pe_signal():
    engine = DecisionEngine()

    market = create_market(24500)

    indicators = IndicatorSet(
        ema_high=24650,
        ema_low=24550,
        vwap=24600,
        rsi=40,
        volume_average=100000,
    )

    decision = engine.evaluate(market, indicators)

    assert decision.signal == Signal.BUY_PE
    assert decision.status == DecisionStatus.VALID
    assert decision.is_tradeable


def test_no_signal():
    engine = DecisionEngine()

    market = create_market(25000)

    indicators = IndicatorSet(
        ema_high=25100,
        ema_low=24900,
        vwap=25000,
        rsi=50,
        volume_average=100000,
    )

    decision = engine.evaluate(market, indicators)

    assert decision.signal == Signal.NONE
    assert decision.status == DecisionStatus.NO_SIGNAL
    assert not decision.is_tradeable
