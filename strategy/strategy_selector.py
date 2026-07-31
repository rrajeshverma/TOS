class StrategySelector:
    """Selects the active strategy from a registry."""

    def select(self, registry):
        if registry is None:
            raise ValueError("registry cannot be None")

        strategies = registry.strategies()

        if not strategies:
            return None

        return strategies[0]
