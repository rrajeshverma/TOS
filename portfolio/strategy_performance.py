class StrategyPerformance:
    def __init__(self):
        self.trades = []

    # --------------------------------------------------
    # Trade Management
    # --------------------------------------------------

    def add_trade(self, pnl):
        self.trades.append(pnl)

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def net_profit(self):
        return sum(self.trades)

    def winning_trades(self):
        return len([t for t in self.trades if t > 0])

    def losing_trades(self):
        return len([t for t in self.trades if t < 0])

    def total_trades(self):
        return len(self.trades)

    def win_rate(self):
        total = self.total_trades()

        if total == 0:
            return 0.0

        return (self.winning_trades() / total) * 100

    # --------------------------------------------------
    # Largest Trades
    # --------------------------------------------------

    def largest_win(self):
        winners = [t for t in self.trades if t > 0]

        if not winners:
            return 0

        return max(winners)

    def largest_loss(self):
        losers = [t for t in self.trades if t < 0]

        if not losers:
            return 0

        return min(losers)

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):
        return {
            "net_profit": self.net_profit(),
            "total_trades": self.total_trades(),
            "winning_trades": self.winning_trades(),
            "losing_trades": self.losing_trades(),
            "win_rate": self.win_rate(),
            "largest_win": self.largest_win(),
            "largest_loss": self.largest_loss(),
        }
