from portfolio.strategy_registry import StrategyRegistry


def test_create_registry():
    registry = StrategyRegistry()

    assert registry is not None


def test_register_strategy():
    registry = StrategyRegistry()

    registry.register(
        "ORB",
        object(),
    )

    assert "ORB" in registry.strategies


def test_get_registered_strategy():
    registry = StrategyRegistry()

    strategy = object()

    registry.register(
        "ORB",
        strategy,
    )

    assert registry.get("ORB") is strategy


def test_contains_registered_strategy():
    registry = StrategyRegistry()

    registry.register(
        "ORB",
        object(),
    )

    assert registry.contains("ORB")


def test_contains_unknown_strategy():
    registry = StrategyRegistry()

    assert not registry.contains("UNKNOWN")


def test_unregister_strategy():
    registry = StrategyRegistry()

    registry.register(
        "ORB",
        object(),
    )

    registry.unregister("ORB")

    assert not registry.contains("ORB")


def test_list_strategies():
    registry = StrategyRegistry()

    registry.register(
        "ORB",
        object(),
    )
    registry.register(
        "VWAP",
        object(),
    )

    assert registry.list_strategies() == [
        "ORB",
        "VWAP",
    ]
