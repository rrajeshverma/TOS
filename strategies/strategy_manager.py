from strategies.loader import StrategyLoader
from strategies.registry import StrategyRegistry
from strategies.strategy_engine import StrategyEngine


class StrategyManager:
    def __init__(self):
        self.registry = StrategyRegistry()
        self.engine = StrategyEngine(self.registry)
        self.loader = StrategyLoader()

    def initialize(self):
        """
        Discover and register all available strategy plugins.
        """
        for strategy in self.loader.instances():
            self.registry.register(
                strategy.name(),
                strategy,
            )