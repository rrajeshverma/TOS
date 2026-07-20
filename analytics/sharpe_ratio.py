import statistics


class SharpeRatio:
    """Calculates the Sharpe Ratio."""

    def calculate(
        self,
        returns: list[float],
        risk_free_rate: float = 0.0,
    ) -> float:

        if len(returns) < 2:
            return 0.0

        excess_returns = [
            value - risk_free_rate
            for value in returns
        ]

        mean_return = statistics.mean(
            excess_returns
        )

        std_dev = statistics.stdev(
            excess_returns
        )

        if std_dev == 0:
            return 0.0

        return mean_return / std_dev