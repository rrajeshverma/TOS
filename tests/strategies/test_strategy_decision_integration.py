from strategies.decision import StrategyDecision
from strategies.nifty_orb import NiftyORBStrategy
from strategies.registry import StrategyRegistry
from strategies.strategy_engine import StrategyEngine


def create_engine():
    registry = StrategyRegistry()

    registry.register(
        "NIFTY_ORB",
        NiftyORBStrategy(),
    )

    return StrategyEngine(registry)


def test_engine_returns_strategy_decision():
    engine = create_engine()

    decision = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "current_price": 24510,
        },
    )

    assert isinstance(
        decision,
        StrategyDecision,
    )


def test_decision_contains_strategy_name():
    engine = create_engine()

    decision = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "current_price": 24510,
        },
    )

    assert decision.strategy == "NIFTY_ORB"


def test_decision_contains_buy_signal():
    engine = create_engine()

    decision = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "current_price": 24510,
        },
    )

    assert decision.signal == "BUY"


def test_decision_has_confidence():
    engine = create_engine()

    decision = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "current_price": 24510,
        },
    )

    assert decision.confidence > 0


def test_decision_contains_metadata():
    engine = create_engine()

    decision = engine.execute(
        "NIFTY_ORB",
        {
            "opening_high": 24500,
            "current_price": 24510,
        },
    )

    assert isinstance(
        decision.metadata,
        dict,
    )


def test_unknown_strategy_returns_none():
    engine = create_engine()

    decision = engine.execute(
        "UNKNOWN",
        {},
    )

    assert decision is None
