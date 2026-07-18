class StrategyPipeline:
    def __init__(self):
        self._strategies = []

    def add(self, strategy):
        self._strategies.append(strategy)

    def remove(self, strategy):
        if strategy in self._strategies:
            self._strategies.remove(strategy)

    def clear(self):
        self._strategies.clear()

    def count(self):
        return len(self._strategies)

    def is_empty(self):
        return self.count() == 0

    def strategies(self):
        return list(self._strategies)

    def execute(self, context=None):
        results = []

        for strategy in self._strategies:
            if context is None:
                results.append(strategy.execute())
            else:
                results.append(strategy.execute(context))

        return results

    def contains(self, strategy):
        return strategy in self._strategies

    def first(self):
        if self._strategies:
            return self._strategies[0]

        return None

    def last(self):
        if self._strategies:
            return self._strategies[-1]

        return None