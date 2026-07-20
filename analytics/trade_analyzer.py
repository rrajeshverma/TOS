class TradeAnalyzer:
    def largest_win(self, trades):
        wins = [trade for trade in trades if trade > 0]
        return max(wins) if wins else 0

    def largest_loss(self, trades):
        losses = [trade for trade in trades if trade < 0]
        return min(losses) if losses else 0

    def max_consecutive_wins(self, trades):
        maximum = current = 0

        for trade in trades:
            if trade > 0:
                current += 1
                maximum = max(maximum, current)
            else:
                current = 0

        return maximum

    def max_consecutive_losses(self, trades):
        maximum = current = 0

        for trade in trades:
            if trade < 0:
                current += 1
                maximum = max(maximum, current)
            else:
                current = 0

        return maximum
    
    def analyze(self, trades):
        return {
            "trade_count": len(trades),
            "winning_trades": sum(1 for trade in trades if trade > 0),
            "losing_trades": sum(1 for trade in trades if trade < 0),
            "largest_win": self.largest_win(trades),
            "largest_loss": self.largest_loss(trades),
            "max_consecutive_wins": self.max_consecutive_wins(trades),
            "max_consecutive_losses": self.max_consecutive_losses(trades),
        }