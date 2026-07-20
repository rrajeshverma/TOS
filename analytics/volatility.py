import statistics


class Volatility:
    """Calculates return volatility."""

    def calculate(
        self,
        returns: list[float],
    ) -> float:

        if len(returns) < 2:
            return 0.0

        return statistics.stdev(returns)