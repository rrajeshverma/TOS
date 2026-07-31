import math


class ValueAtRisk:
    """Calculates Historical Value at Risk."""

    def calculate(
        self,
        returns: list[float],
        confidence: float = 0.95,
    ) -> float:
        if not returns:
            return 0.0

        sorted_returns = sorted(returns)

        index = math.floor((1 - confidence) * (len(sorted_returns) - 1))

        var = sorted_returns[index]

        return abs(min(var, 0.0))
