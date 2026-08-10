import pytest

from strategy.orb_strategy import OrbStrategy
from strategy.strategy_registry import StrategyRegistry
from strategy.strategy_selector import StrategySelector


def test_can_create_selector():
    assert StrategySelector() is not None


def test_returns_none_when_registry_empty():
    selector = StrategySelector()
    registry = StrategyRegistry()

    assert selector.select(registry) is None


def test_returns_registered_strategy():
    selector = StrategySelector()
    registry = StrategyRegistry()

    strategy = OrbStrategy()
    registry.register(strategy)

    assert selector.select(registry) is strategy


def test_returns_first_registered_strategy():
    selector = StrategySelector()
    registry = StrategyRegistry()

    first = OrbStrategy()
    second = OrbStrategy()

    registry.register(first)
    registry.register(second)

    assert selector.select(registry) is first


def test_repeatable():
    selector = StrategySelector()
    registry = StrategyRegistry()

    strategy = OrbStrategy()
    registry.register(strategy)

    assert selector.select(registry) is selector.select(registry)


def test_stateless():
    selector = StrategySelector()

    assert vars(selector) == {}


def test_rejects_none_registry():
    selector = StrategySelector()

    with pytest.raises(ValueError):
        selector.select(None)
