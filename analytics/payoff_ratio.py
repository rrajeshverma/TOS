class PayoffRatio:
    """Calculates the Payoff Ratio."""

    def calculate(
        self,
        average_win: float,
        average_loss: float,
    ) -> float:

        if average_win == 0:
            return 0.0

        loss = abs(average_loss)

        if loss == 0:
            return 0.0

        return average_win / loss
