from strategies.nifty_orb import NiftyORBStrategy
from strategies.registry import StrategyRegistry
from strategies.strategy_engine import StrategyEngine


def create_engine():

    registry = StrategyRegistry()

    registry.register(
        "NIFTY_ORB",
        NiftyORBStrategy(),
    )

    return StrategyEngine(
        registry
    )


def test_engine_can_execute_strategy():

    engine = create_engine()

    result = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "current_price": 24510,
        },
    )

    assert result.signal == "BUY"


def test_engine_returns_sell_signal():

    engine = create_engine()

    result = engine.execute(
        "NIFTY_ORB",
        {
            "opening_low": 24500,
            "current_price": 24490,
        },
    )

    assert result.signal == "SELL"


def test_engine_returns_wait_signal():

    engine = create_engine()

    result = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "opening_low": 24400,
            "current_price": 24450,
        },
    )

    assert result.signal == "WAIT"


def test_engine_rejects_unknown_strategy():

    engine = create_engine()

    assert (
        engine.execute(
            "UNKNOWN",
            {},
        )
        is None
    )


def test_engine_requires_registry():

    try:
        StrategyEngine(None)
        assert False

    except ValueError:
        assert True


def test_engine_can_analyze_strategy():

    engine = create_engine()

    result = engine.analyze(
        "NIFTY_ORB",
        {},
    )

    assert result is not None
