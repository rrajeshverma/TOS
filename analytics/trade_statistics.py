class TradeStatistics:
    def __init__(self, trades):
        if not trades:
            self.profit_factor = 0
            self.expectancy = 0
            return

        gross_profit = sum(t["pnl"] for t in trades if t["pnl"] > 0)
        gross_loss = -sum(t["pnl"] for t in trades if t["pnl"] < 0)

        self.profit_factor = (
            gross_profit / gross_loss
            if gross_loss
            else 0
        )

        self.expectancy = (
            (gross_profit - gross_loss)
            / len(trades)
        )
