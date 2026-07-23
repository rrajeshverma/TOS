class RecoveryRatio:
    """Calculates the Recovery Ratio."""

    def calculate(
        self,
        net_profit: float,
        max_drawdown: float,
    ) -> float:
        if net_profit == 0:
            return 0.0

        drawdown = abs(max_drawdown)

        if drawdown == 0:
            return 0.0

        return net_profit / drawdown
