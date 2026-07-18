class StrategyRegistry:
    def __init__(self):
        self.strategies = {}

    def register(self, name, strategy):
        self.strategies[name] = strategy

    def get(self, name):
        return self.strategies.get(name)

    def contains(self, name):
        return name in self.strategies

    def unregister(self, name):
        self.strategies.pop(name, None)

    def list_strategies(self):
        return list(self.strategies.keys())