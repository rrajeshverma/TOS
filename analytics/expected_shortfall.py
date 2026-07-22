import math


class ExpectedShortfall:
    """Calculates Historical Expected Shortfall."""

    def calculate(
        self,
        returns: list[float],
        confidence: float = 0.95,
    ) -> float:

        if not returns:
            return 0.0

        sorted_returns = sorted(returns)

        cutoff = math.floor((1 - confidence) * len(sorted_returns))

        tail = sorted_returns[: max(1, cutoff)]

        losses = [value for value in tail if value < 0]

        if not losses:
            return 0.0

        return abs(sum(losses) / len(losses))
