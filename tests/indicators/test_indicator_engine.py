from inspect import signature

import pytest

from domain.indicator_set import IndicatorSet
from indicators.indicator_engine import IndicatorEngine
from market.market_runtime import MarketRuntime


def test_can_create_indicator_engine():
    engine = IndicatorEngine()

    assert engine is not None


def test_indicator_engine_has_no_initial_state():
    engine = IndicatorEngine()

    assert vars(engine) == {}


def test_calculate_method_exists():
    engine = IndicatorEngine()

    assert hasattr(engine, "calculate")


def test_calculate_is_callable():
    engine = IndicatorEngine()

    assert callable(engine.calculate)


def test_calculate_accepts_one_argument():
    params = list(signature(IndicatorEngine.calculate).parameters.values())

    assert len(params) == 2  # self + runtime


def test_calculate_returns_indicator_set():
    runtime = MarketRuntime()

    engine = IndicatorEngine()

    result = engine.calculate(runtime)

    assert isinstance(result, IndicatorSet)


def test_calculate_never_returns_none():
    runtime = MarketRuntime()

    engine = IndicatorEngine()

    assert engine.calculate(runtime) is not None


def test_calculate_rejects_none_runtime():
    engine = IndicatorEngine()

    with pytest.raises(ValueError):
        engine.calculate(None)


def test_calculate_rejects_invalid_runtime():
    engine = IndicatorEngine()

    with pytest.raises(TypeError):
        engine.calculate(object())


def test_calculate_accepts_market_runtime():
    runtime = MarketRuntime()

    engine = IndicatorEngine()

    engine.calculate(runtime)


def test_calculate_does_not_change_runtime_running_state():
    runtime = MarketRuntime()

    before = runtime.is_running()

    IndicatorEngine().calculate(runtime)

    after = runtime.is_running()

    assert before == after


def test_calculate_does_not_change_runtime_feed():
    runtime = MarketRuntime(feed="dummy")

    before = runtime.feed

    IndicatorEngine().calculate(runtime)

    assert runtime.feed == before


def test_calculate_is_repeatable():
    runtime = MarketRuntime()

    engine = IndicatorEngine()

    first = engine.calculate(runtime)
    second = engine.calculate(runtime)

    assert first == second


def test_calculate_does_not_store_internal_state():
    runtime = MarketRuntime()

    engine = IndicatorEngine()

    engine.calculate(runtime)

    assert vars(engine) == {}


def test_calculate_returns_float_ema_high():
    result = IndicatorEngine().calculate(MarketRuntime())

    assert isinstance(result.ema_high, float)


def test_calculate_returns_float_ema_low():
    result = IndicatorEngine().calculate(MarketRuntime())

    assert isinstance(result.ema_low, float)


def test_calculate_returns_float_vwap():
    result = IndicatorEngine().calculate(MarketRuntime())

    assert isinstance(result.vwap, float)


def test_calculate_returns_float_rsi():
    result = IndicatorEngine().calculate(MarketRuntime())

    assert isinstance(result.rsi, float)


def test_calculate_returns_float_volume_average():
    result = IndicatorEngine().calculate(MarketRuntime())

    assert isinstance(result.volume_average, float)


def test_calculate_returns_immutable_indicator_set():
    result = IndicatorEngine().calculate(MarketRuntime())

    with pytest.raises(Exception):
        result.rsi = 90.0
