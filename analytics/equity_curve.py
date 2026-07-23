class EquityCurve:
    def __init__(self, initial_capital, trades):
        self.points = [initial_capital]

        equity = initial_capital
        for pnl in trades:
            equity += pnl
            self.points.append(equity)
