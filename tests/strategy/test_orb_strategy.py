import pytest

from domain.indicator_set import IndicatorSet
from strategy.orb_strategy import OrbStrategy


def indicators(rsi=50.0):
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=rsi,
        volume_average=1000.0,
    )


def test_can_create_orb_strategy():
    assert OrbStrategy() is not None


def test_has_decide_method():
    strategy = OrbStrategy()
    assert callable(strategy.decide)


def test_rejects_none():
    strategy = OrbStrategy()

    with pytest.raises(ValueError):
        strategy.decide(None)


def test_returns_string():
    strategy = OrbStrategy()

    result = strategy.decide(indicators())

    assert isinstance(result, str)


def test_repeatable():
    strategy = OrbStrategy()
    data = indicators()

    assert strategy.decide(data) == strategy.decide(data)


def test_stateless():
    strategy = OrbStrategy()

    strategy.decide(indicators())

    assert vars(strategy) == {}
