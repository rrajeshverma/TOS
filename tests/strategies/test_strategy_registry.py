import pytest

from strategies.registry import StrategyRegistry


class DummyStrategy:

    def name(self):
        return "DUMMY"


def test_registry_can_register_strategy():

    registry = StrategyRegistry()

    strategy = DummyStrategy()

    registry.register(
        "DUMMY",
        strategy,
    )

    assert (
        registry.get("DUMMY")
        == strategy
    )


def test_registry_returns_none_for_unknown_strategy():

    registry = StrategyRegistry()

    assert (
        registry.get("UNKNOWN")
        is None
    )


def test_registry_lists_strategies():

    registry = StrategyRegistry()

    registry.register(
        "DUMMY",
        DummyStrategy(),
    )

    assert (
        "DUMMY"
        in registry.list()
    )


def test_registry_removes_strategy():

    registry = StrategyRegistry()

    registry.register(
        "DUMMY",
        DummyStrategy(),
    )

    registry.remove("DUMMY")

    assert (
        registry.get("DUMMY")
        is None
    )


def test_registry_requires_strategy_name():

    registry = StrategyRegistry()

    with pytest.raises(ValueError):

        registry.register(
            "",
            DummyStrategy(),
        )


def test_registry_requires_strategy_object():

    registry = StrategyRegistry()

    with pytest.raises(ValueError):

        registry.register(
            "DUMMY",
            None,
        )
