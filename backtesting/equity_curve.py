class EquityCurve:
    def __init__(self, trades):
        self.trades = trades

    def values(self):
        equity = 0
        curve = []

        for trade in self.trades:
            equity += trade["pnl"]
            curve.append(equity)

        return curve