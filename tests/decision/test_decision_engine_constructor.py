from decision.decision_engine import DecisionEngine
from strategy.strategy_registry import StrategyRegistry


def test_accepts_registry():
    registry = StrategyRegistry()

    engine = DecisionEngine(registry)

    assert engine is not None


def test_accepts_none_registry():
    engine = DecisionEngine(None)

    assert engine is not None


def test_stores_registry():
    registry = StrategyRegistry()

    engine = DecisionEngine(registry)

    assert engine._registry is registry
