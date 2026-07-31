class TradePerformanceReport:
    def __init__(self, trades):
        self.total_trades = len(trades)

        self.winning_trades = sum(1 for t in trades if t["pnl"] > 0)
        self.losing_trades = sum(1 for t in trades if t["pnl"] < 0)

        self.gross_profit = sum(t["pnl"] for t in trades if t["pnl"] > 0)
        self.gross_loss = -sum(t["pnl"] for t in trades if t["pnl"] < 0)

        self.net_profit = self.gross_profit - self.gross_loss

        self.win_rate = (
            (self.winning_trades / self.total_trades) * 100 if self.total_trades else 0
        )
