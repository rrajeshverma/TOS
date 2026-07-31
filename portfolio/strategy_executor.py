class StrategyExecutor:
    def execute(
        self,
        strategy,
        context=None,
    ):
        if context is None:
            return strategy.execute()

        return strategy.execute(context)

    def execute_many(
        self,
        strategies,
        context=None,
    ):
        results = []

        for strategy in strategies:
            results.append(
                self.execute(
                    strategy,
                    context,
                )
            )

        return results

    def execute_first(
        self,
        strategies,
        context=None,
    ):
        if not strategies:
            return None

        return self.execute(
            strategies[0],
            context,
        )

    def execute_last(
        self,
        strategies,
        context=None,
    ):
        if not strategies:
            return None

        return self.execute(
            strategies[-1],
            context,
        )

    def count(
        self,
        strategies,
    ):
        return len(strategies)
