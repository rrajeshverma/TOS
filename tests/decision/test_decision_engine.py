import pytest

from decision.decision_engine import DecisionEngine
from domain.indicator_set import IndicatorSet
from strategy.strategy_registry import StrategyRegistry


def indicator_set(
    ema_high=100.0,
    ema_low=95.0,
    vwap=98.0,
    rsi=50.0,
    volume_average=1000.0,
):
    return IndicatorSet(
        ema_high=ema_high,
        ema_low=ema_low,
        vwap=vwap,
        rsi=rsi,
        volume_average=volume_average,
    )


def test_can_create_decision_engine():
    assert DecisionEngine() is not None


def test_has_decide_method():
    engine = DecisionEngine()

    assert callable(engine.decide)


def test_rejects_none_indicator_set():
    engine = DecisionEngine()

    with pytest.raises(ValueError):
        engine.decide(None)


def test_returns_decision():
    engine = DecisionEngine()

    result = engine.decide(indicator_set())

    assert result is not None


def test_repeatable():
    engine = DecisionEngine()

    indicators = indicator_set()

    assert engine.decide(indicators) == engine.decide(indicators)


def test_stateless():
    engine = DecisionEngine()

    engine.decide(indicator_set())

    assert isinstance(engine._registry, StrategyRegistry)
