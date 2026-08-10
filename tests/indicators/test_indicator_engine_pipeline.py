from domain.indicator_set import IndicatorSet
from indicators.indicator_engine import IndicatorEngine
from market.market_runtime import MarketRuntime


def test_pipeline_returns_indicator_set():
    engine = IndicatorEngine()

    result = engine.calculate(MarketRuntime())

    assert isinstance(result, IndicatorSet)


def test_pipeline_returns_all_float_values():
    engine = IndicatorEngine()

    result = engine.calculate(MarketRuntime())

    assert isinstance(result.ema_high, float)
    assert isinstance(result.ema_low, float)
    assert isinstance(result.vwap, float)
    assert isinstance(result.rsi, float)
    assert isinstance(result.volume_average, float)


def test_pipeline_rsi_in_valid_range():
    engine = IndicatorEngine()

    result = engine.calculate(MarketRuntime())

    assert 0.0 <= result.rsi <= 100.0


def test_pipeline_repeatable():
    engine = IndicatorEngine()
    runtime = MarketRuntime()

    assert engine.calculate(runtime) == engine.calculate(runtime)


def test_pipeline_engine_stateless():
    engine = IndicatorEngine()

    engine.calculate(MarketRuntime())

    assert vars(engine) == {}
