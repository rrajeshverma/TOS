from strategy.strategy_registry import StrategyRegistry


class DecisionEngine:
    def __init__(self, registry=None):
        self._registry = registry or StrategyRegistry()

    def decide(self, indicators):
        if indicators is None:
            raise ValueError("indicators cannot be None")

        strategies = self._registry.strategies()

        if not strategies:
            if indicators.rsi < 30:
                return "BUY"

            if indicators.rsi > 70:
                return "SELL"

            return "HOLD"

        return strategies[0].decide(indicators)
