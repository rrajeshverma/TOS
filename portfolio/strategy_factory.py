from portfolio.strategy_loader import StrategyLoader


class StrategyFactory:
    def __init__(self):
        self.loader = StrategyLoader()

    def register(self, name, strategy):
        self.loader.register(name, strategy)

    def create(self, name):
        return self.loader.get(name)

    def create_all(self):
        return [self.loader.get(name) for name in self.loader.list_strategies()]

    def contains(self, name):
        return self.loader.contains(name)

    def count(self):
        return self.loader.count()

    def clear(self):
        self.loader.clear()

    def list_strategies(self):
        return self.loader.list_strategies()
