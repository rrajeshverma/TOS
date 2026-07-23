import math
import statistics


class SortinoRatio:
    """Calculates the Sortino Ratio."""

    def calculate(
        self,
        returns: list[float],
        risk_free_rate: float = 0.0,
    ) -> float:
        if len(returns) < 2:
            return 0.0

        excess_returns = [value - risk_free_rate for value in returns]

        mean_return = statistics.mean(excess_returns)

        downside_returns = [value for value in excess_returns if value < 0]

        if len(downside_returns) < 2:
            return 0.0

        downside_deviation = statistics.stdev(downside_returns)

        if math.isclose(
            downside_deviation,
            0.0,
            abs_tol=1e-12,
        ):
            return 0.0

        return mean_return / downside_deviation
