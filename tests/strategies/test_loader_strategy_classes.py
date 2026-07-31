import inspect

from strategies.base_strategy import BaseStrategy
from strategies.loader import StrategyLoader


def test_loader_finds_strategy_classes():
    loader = StrategyLoader()

    classes = loader.strategy_classes()

    assert len(classes) > 0

    for cls in classes:
        assert inspect.isclass(cls)
        assert issubclass(cls, BaseStrategy)
        assert cls is not BaseStrategy
