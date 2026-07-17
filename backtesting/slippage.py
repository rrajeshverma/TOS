class Slippage:
    def __init__(self, amount=0):
        self.amount = amount

    def apply(self, trade):
        trade = trade.copy()

        if trade["action"] == "BUY":
            trade["entry_price"] += self.amount
        elif trade["action"] == "SELL":
            trade["entry_price"] -= self.amount
        else:
            raise ValueError(f"Unknown action: {trade['action']}")

        return trade