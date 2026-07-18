from portfolio.strategy_registry import StrategyRegistry


class StrategyLoader:
    def __init__(self):
        self.registry = StrategyRegistry()

    def register(self, name, strategy):
        self.registry.register(name, strategy)

    def unregister(self, name):
        self.registry.unregister(name)

    def get(self, name):
        return self.registry.get(name)

    def contains(self, name):
        return self.registry.contains(name)

    def load_many(self, strategies):
        for name, strategy in strategies.items():
            self.register(name, strategy)

    def load(self, strategies):
        self.load_many(strategies)

    def list_strategies(self):
        return self.registry.list_strategies()

    def count(self):
        return len(self.registry.list_strategies())

    def is_empty(self):
        return self.count() == 0

    def clear(self):
        self.registry.strategies.clear()