import pytest

from decision.decision_engine import DecisionEngine
from domain.indicator_set import IndicatorSet


def indicators(rsi=50.0):
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=rsi,
        volume_average=1000.0,
    )


@pytest.mark.parametrize(
    "rsi,expected",
    [
        (0.0, "BUY"),
        (10.0, "BUY"),
        (29.9, "BUY"),
        (30.0, "HOLD"),
        (40.0, "HOLD"),
        (50.0, "HOLD"),
        (60.0, "HOLD"),
        (70.0, "HOLD"),
        (70.1, "SELL"),
        (80.0, "SELL"),
        (90.0, "SELL"),
        (100.0, "SELL"),
    ],
)
def test_decision_boundaries(rsi, expected):
    engine = DecisionEngine()
    assert engine.decide(indicators(rsi=rsi)) == expected


def test_repeatable_buy():
    engine = DecisionEngine()
    data = indicators(25.0)
    assert engine.decide(data) == engine.decide(data)


def test_repeatable_sell():
    engine = DecisionEngine()
    data = indicators(75.0)
    assert engine.decide(data) == engine.decide(data)


def test_repeatable_hold():
    engine = DecisionEngine()
    data = indicators(50.0)
    assert engine.decide(data) == engine.decide(data)
