from strategies.strategy_manager import StrategyManager


def test_initialize_registers_all_strategies():
    manager = StrategyManager()

    manager.initialize()

    assert len(manager.registry.list()) > 0
