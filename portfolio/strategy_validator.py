class StrategyValidator:
    def is_valid_name(
        self,
        name,
    ):
        return (
            isinstance(name, str)
            and bool(name.strip())
        )

    def is_valid_strategy(
        self,
        strategy,
    ):
        return (
            strategy is not None
            and hasattr(strategy, "execute")
            and callable(strategy.execute)
        )

    def validate(
        self,
        name,
        strategy,
    ):
        return (
            self.is_valid_name(name)
            and self.is_valid_strategy(strategy)
        )

    def validate_many(
        self,
        strategies,
    ):
        return all(
            self.validate(name, strategy)
            for name, strategy in strategies.items()
        )