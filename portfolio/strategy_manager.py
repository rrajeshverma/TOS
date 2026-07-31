from portfolio.strategy_registry import StrategyRegistry


class StrategyManager:
    def __init__(self):
        self.registry = StrategyRegistry()
        self.enabled_strategies = set()

    def register(
        self,
        name,
        strategy,
    ):
        self.registry.register(
            name,
            strategy,
        )

    def get(
        self,
        name,
    ):
        return self.registry.get(name)

    def enable(
        self,
        name,
    ):
        self.enabled_strategies.add(name)

    def disable(
        self,
        name,
    ):
        self.enabled_strategies.discard(name)

    def is_enabled(
        self,
        name,
    ):
        return name in self.enabled_strategies

    def list_enabled_strategies(
        self,
    ):
        return list(self.enabled_strategies)

    def execute(
        self,
        name,
    ):
        if self.is_enabled(name):
            strategy = self.get(name)

            if strategy is not None:
                return strategy.execute()

        return None

    def execute_all(
        self,
    ):
        results = {}

        for name in self.enabled_strategies:
            try:
                results[name] = self.execute(name)
            except Exception:
                results[name] = None

        return results

    def disable_all(
        self,
    ):
        self.enabled_strategies.clear()

    def enable_all(
        self,
    ):
        self.enabled_strategies = set(self.registry.list_strategies())

    def has_enabled_strategies(
        self,
    ):
        return bool(self.enabled_strategies)

    def remove(
        self,
        name,
    ):
        self.disable(name)
        self.registry.unregister(name)
