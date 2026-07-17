class TradeSimulator:
    def __init__(self):
        self.position = None
        self.trades = []

    def open(self, signal):
        if self.position is not None:
            raise RuntimeError("Position already open.")

        self.position = {
            "action": signal["action"],
            "entry_price": signal["price"],
        }

    def close(self, exit_price):
        if self.position is None:
            raise RuntimeError("No open position.")

        entry_price = self.position["entry_price"]
        action = self.position["action"]

        if action == "BUY":
            pnl = exit_price - entry_price
        elif action == "SELL":
            pnl = entry_price - exit_price
        else:
            raise ValueError(f"Unknown action: {action}")

        trade = {
            "action": action,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": pnl,
        }

        self.trades.append(trade)
        self.position = None