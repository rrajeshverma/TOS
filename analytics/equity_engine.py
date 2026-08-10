class EquityEngine:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.current_equity = initial_capital
        self.peak_equity = initial_capital
        self.equity_history = [initial_capital]

    def record_trade(self, pnl):
        self.current_equity += pnl

        self.peak_equity = max(self.peak_equity, self.current_equity)

        self.equity_history.append(self.current_equity)
