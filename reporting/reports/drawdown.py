class Drawdown:
    """Calculates maximum drawdown from an equity curve."""

    def calculate(
        self,
        equity_curve: list[float],
    ) -> float:

        if len(equity_curve) <= 1:
            return 0.0

        peak = equity_curve[0]
        max_drawdown = 0.0

        for equity in equity_curve:

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown