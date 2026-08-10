import pytest

from strategy.orb_strategy import OrbStrategy
from strategy.strategy_factory import StrategyFactory


def test_can_create_factory():
    assert StrategyFactory() is not None


def test_returns_orb_strategy():
    factory = StrategyFactory()

    strategy = factory.create("ORB")

    assert isinstance(strategy, OrbStrategy)


def test_unknown_strategy_raises():
    factory = StrategyFactory()

    with pytest.raises(ValueError):
        factory.create("UNKNOWN")


def test_repeatable():
    factory = StrategyFactory()

    first = factory.create("ORB")
    second = factory.create("ORB")

    assert type(first) is type(second)


def test_stateless():
    factory = StrategyFactory()

    factory.create("ORB")

    assert vars(factory) == {}
