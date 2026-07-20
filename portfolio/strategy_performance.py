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
    
        # --------------------------------------------------
    # Gross Profit / Loss
    # --------------------------------------------------

    def gross_profit(self):
        return sum(t for t in self.trades if t > 0)

    def gross_loss(self):
        return abs(sum(t for t in self.trades if t < 0))

    # --------------------------------------------------
    # Average Win / Loss
    # --------------------------------------------------

    def average_win(self):
        winners = [t for t in self.trades if t > 0]

        if not winners:
            return 0

        return sum(winners) / len(winners)

    def average_loss(self):
        losers = [abs(t) for t in self.trades if t < 0]

        if not losers:
            return 0

        return sum(losers) / len(losers)

    # --------------------------------------------------
    # Profit Factor
    # --------------------------------------------------

    def profit_factor(self):
        gross_loss = self.gross_loss()

        if gross_loss == 0:
            return float("inf")

        return self.gross_profit() / gross_loss

    # --------------------------------------------------
    # Expectancy
    # --------------------------------------------------

    def expectancy(self):
        if self.total_trades() == 0:
            return 0

        return self.net_profit() / self.total_trades()

    # --------------------------------------------------
    # Consecutive Wins / Losses
    # --------------------------------------------------

    def max_consecutive_wins(self):
        current = 0
        maximum = 0

        for trade in self.trades:
            if trade > 0:
                current += 1
                maximum = max(maximum, current)
            else:
                current = 0

        return maximum

    def max_consecutive_losses(self):
        current = 0
        maximum = 0

        for trade in self.trades:
            if trade < 0:
                current += 1
                maximum = max(maximum, current)
            else:
                current = 0

        return maximum