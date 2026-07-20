class EquityAnalytics:
    def __init__(self, initial_equity):
        self.initial_equity = initial_equity
        self._curve = [initial_equity]

    # --------------------------------------------------
    # Trade Management
    # --------------------------------------------------

    def add_trade(self, pnl):
        self._curve.append(self._curve[-1] + pnl)

    # --------------------------------------------------
    # Equity Curve
    # --------------------------------------------------

    def equity_curve(self):
        return self._curve.copy()

    def current_equity(self):
        return self._curve[-1]

    def peak_equity(self):
        return max(self._curve)

    # --------------------------------------------------
    # Returns
    # --------------------------------------------------

    def total_return(self):
        return self.current_equity() - self.initial_equity

    def return_percent(self):
        if self.initial_equity == 0:
            return 0.0

        return (self.total_return() / self.initial_equity) * 100

    # --------------------------------------------------
    # Drawdown
    # --------------------------------------------------

    def max_drawdown(self):
        peak = self._curve[0]
        maximum_drawdown = 0

        for equity in self._curve:
            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > maximum_drawdown:
                maximum_drawdown = drawdown

        return maximum_drawdown

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):
        return {
            "initial_equity": self.initial_equity,
            "current_equity": self.current_equity(),
            "peak_equity": self.peak_equity(),
            "max_drawdown": self.max_drawdown(),
            "total_return": self.total_return(),
            "return_percent": self.return_percent(),
        }