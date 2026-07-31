class CalmarRatio:
    """Calculates the Calmar Ratio."""

    def calculate(
        self,
        annual_return: float,
        max_drawdown: float,
    ) -> float:
        if annual_return == 0:
            return 0.0

        drawdown = abs(max_drawdown)

        if drawdown == 0:
            return 0.0

        return annual_return / drawdown
