class TradeHistory:
    def __init__(self):
        self.trades = []

    def record_trade(self, trade):
        self.trades.append(trade)

    def get_all(self):
        return self.trades

    def summary(self):
        total_pnl = sum(t["pnl"] for t in self.trades)
        wins = sum(1 for t in self.trades if t["pnl"] > 0)
        losses = sum(1 for t in self.trades if t["pnl"] <= 0)

        return {
            "total_trades": len(self.trades),
            "total_pnl": total_pnl,
            "wins": wins,
            "losses": losses,
        }
