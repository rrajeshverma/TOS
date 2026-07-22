import pytest

from portfolio.strategy_manager import StrategyManager


class DummyStrategy:
    def execute(self):
        return "OK"


class FailingStrategy:
    def execute(self):
        raise RuntimeError("boom")


def test_execute_returns_none_when_strategy_disabled():
    manager = StrategyManager()
    manager.register("s1", DummyStrategy())

    assert manager.execute("s1") is None


def test_execute_returns_none_when_strategy_missing():
    manager = StrategyManager()

    assert manager.execute("missing") is None


def test_disable_all_clears_enabled_strategies():
    manager = StrategyManager()

    manager.register("s1", DummyStrategy())
    manager.enable("s1")

    manager.disable_all()

    assert manager.has_enabled_strategies() is False


def test_enable_all_enables_every_registered_strategy():
    manager = StrategyManager()

    manager.register("s1", DummyStrategy())
    manager.register("s2", DummyStrategy())

    manager.enable_all()

    assert manager.is_enabled("s1")
    assert manager.is_enabled("s2")


def test_execute_all_handles_strategy_exception():
    manager = StrategyManager()

    manager.register("good", DummyStrategy())
    manager.register("bad", FailingStrategy())

    manager.enable_all()

    results = manager.execute_all()

    assert results["good"] == "OK"
    assert results["bad"] is None


def test_remove_unregisters_strategy():
    manager = StrategyManager()

    manager.register("s1", DummyStrategy())
    manager.enable("s1")

    manager.remove("s1")

    assert not manager.is_enabled("s1")
    assert manager.get("s1") is None
