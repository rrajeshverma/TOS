class Commission:
    def __init__(self, amount=0):
        self.amount = amount

    def apply(self, trade):
        trade = trade.copy()
        trade["pnl"] -= self.amount
        return trade
