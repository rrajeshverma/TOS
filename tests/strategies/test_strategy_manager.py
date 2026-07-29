from strategies.strategy_manager import StrategyManager


def test_manager_can_be_created():
    manager = StrategyManager()

    assert manager is not None


def test_manager_has_registry():
    manager = StrategyManager()

    assert manager.registry is not None


def test_manager_has_engine():
    manager = StrategyManager()

    assert manager.engine is not None
