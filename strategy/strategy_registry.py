class StrategyRegistry:
    """Stores available trading strategies."""

    def __init__(self):
        self._strategies = []

    def register(self, strategy):
        if strategy is None:
            raise ValueError("strategy cannot be None")

        self._strategies.append(strategy)

    def strategies(self):
        return list(self._strategies)
