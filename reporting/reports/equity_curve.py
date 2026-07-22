class EquityCurve:
    """Builds a cumulative equity curve from trade PnL."""

    def build(
        self,
        pnl_values: list[float],
    ) -> list[float]:

        equity = []
        running = 0

        for pnl in pnl_values:
            running += pnl
            equity.append(running)

        return equity
