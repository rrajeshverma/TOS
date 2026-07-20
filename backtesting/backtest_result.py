class BacktestResult:
    """
    Stores the results of a completed backtest.

    This class will grow in later sprints to include:
    - Gross Profit
    - Gross Loss
    - Win Rate
    - Profit Factor
    - Drawdown
    - Sharpe Ratio
    - Equity Curve
    """

    def __init__(self):
        self.trades = []
        self.net_pnl = 0

    @property
    def total_trades(self):
        return len(self.trades)

    def add_trade(self, trade):
        self.trades.append(trade)
        self.net_pnl += trade["pnl"]
