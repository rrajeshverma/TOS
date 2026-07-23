from indicators.indicator_engine import IndicatorEngine
from market.market_runtime import MarketRuntime
from domain.indicator_set import IndicatorSet


def test_indicator_engine_returns_indicator_set():
    engine = IndicatorEngine()
    runtime = MarketRuntime()

    result = engine.calculate(runtime)

    assert isinstance(result, IndicatorSet)


def test_indicator_engine_calculate_is_repeatable():
    engine = IndicatorEngine()
    runtime = MarketRuntime()

    first = engine.calculate(runtime)
    second = engine.calculate(runtime)

    assert first == second


def test_indicator_engine_returns_float_ema_values():
    engine = IndicatorEngine()
    runtime = MarketRuntime()

    result = engine.calculate(runtime)

    assert isinstance(result.ema_high, float)
    assert isinstance(result.ema_low, float)
