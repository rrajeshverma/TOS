class TradeStatistics:
    """Statistical calculations for a collection of trades."""

    def total_trades(self, trades: list) -> int:
        return len(trades)

    def winning_trades(self, trades: list) -> int:
        return sum(1 for trade in trades if trade.pnl > 0)

    def losing_trades(self, trades: list) -> int:
        return sum(1 for trade in trades if trade.pnl < 0)

    def gross_profit(self, trades: list) -> float:
        return sum(trade.pnl for trade in trades if trade.pnl > 0)

    def gross_loss(self, trades: list) -> float:
        return abs(sum(trade.pnl for trade in trades if trade.pnl < 0))

    def largest_win(self, trades: list) -> float:
        wins = [trade.pnl for trade in trades if trade.pnl > 0]

        if not wins:
            return 0.0

        return max(wins)

    def largest_loss(self, trades: list) -> float:
        losses = [trade.pnl for trade in trades if trade.pnl < 0]

        if not losses:
            return 0.0

        return abs(min(losses))

    def average_win(self, trades: list) -> float:
        wins = [trade.pnl for trade in trades if trade.pnl > 0]

        if not wins:
            return 0.0

        return sum(wins) / len(wins)

    def average_loss(self, trades: list) -> float:
        losses = [trade.pnl for trade in trades if trade.pnl < 0]

        if not losses:
            return 0.0

        return abs(sum(losses) / len(losses))

    def win_rate(self, trades: list) -> float:
        total = self.total_trades(trades)

        if total == 0:
            return 0.0

        return (self.winning_trades(trades) / total) * 100.0

    def profit_factor(self, trades: list) -> float:
        gross_profit = self.gross_profit(trades)
        gross_loss = self.gross_loss(trades)

        if gross_loss == 0:
            return 0.0

        return gross_profit / gross_loss

    def expectancy(self, trades: list) -> float:
        average_win = float(self.average_win(trades))
        average_loss = float(self.average_loss(trades))
        win_rate = self.win_rate(trades)

        win_probability = win_rate / 100.0
        loss_probability = 1.0 - win_probability

        return (
            (average_win * win_probability)
            - (average_loss * loss_probability)
        )
