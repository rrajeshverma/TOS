import pytest

from strategy.strategy import Strategy
from domain.indicator_set import IndicatorSet


def indicators():
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=50.0,
        volume_average=1000.0,
    )


def test_can_create_strategy():
    assert Strategy() is not None


def test_has_decide_method():
    strategy = Strategy()
    assert callable(strategy.decide)


def test_rejects_none():
    strategy = Strategy()

    with pytest.raises(ValueError):
        strategy.decide(None)


def test_returns_string():
    strategy = Strategy()

    result = strategy.decide(indicators())

    assert isinstance(result, str)


def test_repeatable():
    strategy = Strategy()
    data = indicators()

    assert strategy.decide(data) == strategy.decide(data)


def test_stateless():
    strategy = Strategy()

    strategy.decide(indicators())

    assert vars(strategy) == {}
