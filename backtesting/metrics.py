class Metrics:
    def __init__(self, trades):
        self.trades = trades

    @property
    def total_trades(self):
        return len(self.trades)

    @property
    def winning_trades(self):
        return sum(1 for trade in self.trades if trade["pnl"] > 0)

    @property
    def losing_trades(self):
        return sum(1 for trade in self.trades if trade["pnl"] < 0)

    @property
    def net_pnl(self):
        return sum(trade["pnl"] for trade in self.trades)
