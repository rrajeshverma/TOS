from indicators.indicator_engine import IndicatorEngine
from market.market_runtime import MarketRuntime
from domain.indicator_set import IndicatorSet


def test_calculate_returns_indicator_set():
    engine = IndicatorEngine()

    result = engine.calculate(MarketRuntime())

    assert isinstance(result, IndicatorSet)


def test_returns_float_indicators():
    engine = IndicatorEngine()

    result = engine.calculate(MarketRuntime())

    assert isinstance(result.ema_high, float)
    assert isinstance(result.ema_low, float)
    assert isinstance(result.vwap, float)
    assert isinstance(result.rsi, float)
    assert isinstance(result.volume_average, float)


def test_rsi_between_zero_and_hundred():
    engine = IndicatorEngine()

    result = engine.calculate(MarketRuntime())

    assert 0.0 <= result.rsi <= 100.0


def test_calculate_is_repeatable():
    engine = IndicatorEngine()
    runtime = MarketRuntime()

    first = engine.calculate(runtime)
    second = engine.calculate(runtime)

    assert first == second


def test_engine_is_stateless():
    engine = IndicatorEngine()

    engine.calculate(MarketRuntime())

    assert vars(engine) == {}
