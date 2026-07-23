import pytest

from strategy.strategy_registry import StrategyRegistry
from strategy.strategy import Strategy


def test_can_create_registry():
    assert StrategyRegistry() is not None


def test_registry_starts_empty():
    registry = StrategyRegistry()

    assert registry.strategies() == []


def test_can_register_strategy():
    registry = StrategyRegistry()
    strategy = Strategy()

    registry.register(strategy)

    assert strategy in registry.strategies()


def test_rejects_none_strategy():
    registry = StrategyRegistry()

    with pytest.raises(ValueError):
        registry.register(None)


def test_registered_count():
    registry = StrategyRegistry()

    registry.register(Strategy())
    registry.register(Strategy())

    assert len(registry.strategies()) == 2


def test_registry_is_repeatable():
    registry = StrategyRegistry()
    strategy = Strategy()

    registry.register(strategy)

    assert registry.strategies() == registry.strategies()
