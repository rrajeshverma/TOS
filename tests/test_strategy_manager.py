from portfolio.strategy_manager import StrategyManager
from portfolio.strategy_registry import StrategyRegistry


def test_create_strategy_manager():
    manager = StrategyManager()

    assert manager is not None


def test_manager_has_registry():
    manager = StrategyManager()

    assert isinstance(
        manager.registry,
        StrategyRegistry,
    )


def test_manager_register_strategy():
    manager = StrategyManager()

    strategy = object()

    manager.register(
        "ORB",
        strategy,
    )

    assert manager.registry.get("ORB") is strategy


def test_manager_get_strategy():
    manager = StrategyManager()

    strategy = object()

    manager.register(
        "ORB",
        strategy,
    )

    assert manager.get("ORB") is strategy


def test_enable_strategy():
    manager = StrategyManager()

    strategy = object()

    manager.register(
        "ORB",
        strategy,
    )

    manager.enable("ORB")

    assert "ORB" in manager.enabled_strategies


def test_disable_strategy():
    manager = StrategyManager()

    strategy = object()

    manager.register(
        "ORB",
        strategy,
    )

    manager.enable("ORB")
    manager.disable("ORB")

    assert "ORB" not in manager.enabled_strategies


def test_is_enabled():
    manager = StrategyManager()

    manager.register(
        "ORB",
        object(),
    )

    manager.enable("ORB")

    assert manager.is_enabled("ORB") is True
    assert manager.is_enabled("VWAP") is False


def test_list_enabled_strategies():
    manager = StrategyManager()

    manager.register(
        "ORB",
        object(),
    )
    manager.register(
        "VWAP",
        object(),
    )

    manager.enable("ORB")
    manager.enable("VWAP")

    assert sorted(
        manager.list_enabled_strategies(),
    ) == [
        "ORB",
        "VWAP",
    ]


class DummyStrategy:
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True


class DummyResultStrategy:
    def execute(self):
        return "BUY"


class BuyStrategy:
    def execute(self):
        return "BUY"


class SellStrategy:
    def execute(self):
        return "SELL"


class FailingStrategy:
    def execute(self):
        raise RuntimeError("Strategy failed")


def test_execute_enabled_strategy():
    manager = StrategyManager()

    strategy = DummyStrategy()

    manager.register(
        "ORB",
        strategy,
    )

    manager.enable("ORB")

    manager.execute("ORB")

    assert strategy.executed is True


def test_execute_disabled_strategy():
    manager = StrategyManager()

    strategy = DummyStrategy()

    manager.register(
        "ORB",
        strategy,
    )

    manager.execute("ORB")

    assert strategy.executed is False


def test_execute_all_enabled_strategies():
    manager = StrategyManager()

    orb = DummyStrategy()
    vwap = DummyStrategy()

    manager.register(
        "ORB",
        orb,
    )
    manager.register(
        "VWAP",
        vwap,
    )

    manager.enable("ORB")
    manager.enable("VWAP")

    manager.execute_all()

    assert orb.executed is True
    assert vwap.executed is True


def test_execute_returns_result():
    manager = StrategyManager()

    manager.register(
        "ORB",
        DummyResultStrategy(),
    )

    manager.enable("ORB")

    result = manager.execute("ORB")

    assert result == "BUY"


def test_execute_all_returns_results():
    manager = StrategyManager()

    manager.register(
        "ORB",
        BuyStrategy(),
    )
    manager.register(
        "VWAP",
        SellStrategy(),
    )

    manager.enable("ORB")
    manager.enable("VWAP")

    results = manager.execute_all()

    assert results == {
        "ORB": "BUY",
        "VWAP": "SELL",
    }


def test_execute_all_continues_after_exception():
    manager = StrategyManager()

    manager.register(
        "FAIL",
        FailingStrategy(),
    )
    manager.register(
        "BUY",
        BuyStrategy(),
    )

    manager.enable("FAIL")
    manager.enable("BUY")

    results = manager.execute_all()

    assert results["FAIL"] is None
    assert results["BUY"] == "BUY"


def test_disable_all_strategies():
    manager = StrategyManager()

    manager.register(
        "ORB",
        object(),
    )
    manager.register(
        "VWAP",
        object(),
    )

    manager.enable("ORB")
    manager.enable("VWAP")

    manager.disable_all()

    assert manager.list_enabled_strategies() == []


def test_enable_all_strategies():
    manager = StrategyManager()

    manager.register(
        "ORB",
        object(),
    )
    manager.register(
        "VWAP",
        object(),
    )

    manager.enable_all()

    assert sorted(
        manager.list_enabled_strategies(),
    ) == [
        "ORB",
        "VWAP",
    ]


def test_has_enabled_strategies():
    manager = StrategyManager()

    assert manager.has_enabled_strategies() is False

    manager.register(
        "ORB",
        object(),
    )

    manager.enable("ORB")

    assert manager.has_enabled_strategies() is True


def test_remove_strategy():
    manager = StrategyManager()

    strategy = object()

    manager.register(
        "ORB",
        strategy,
    )

    manager.enable("ORB")

    manager.remove("ORB")

    assert manager.get("ORB") is None
    assert manager.is_enabled("ORB") is False
