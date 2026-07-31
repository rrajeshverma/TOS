from strategies.base_strategy import BaseStrategy
from strategies.loader import StrategyLoader


def test_loader_creates_strategy_instances():
    loader = StrategyLoader()

    instances = loader.instances()

    assert len(instances) > 0

    for instance in instances:
        assert isinstance(instance, BaseStrategy)
