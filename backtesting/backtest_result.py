class BacktestResult:
    """
    Stores the results of a completed backtest.
    """

    def __init__(self):
        self.trades = []
        self.net_pnl = 0.0
        self.gross_profit = 0.0
        self.gross_loss = 0.0

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
    def win_rate(self):
        if self.total_trades == 0:
            return 0.0

        return (self.winning_trades / self.total_trades) * 100

    def add_trade(self, trade):
        self.trades.append(trade)

        pnl = trade["pnl"]

        self.net_pnl += pnl

        if pnl > 0:
            self.gross_profit += pnl
        else:
            self.gross_loss += abs(pnl)
