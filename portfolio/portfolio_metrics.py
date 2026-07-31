class PortfolioMetrics:
    def total_pnl(self, snapshot):
        return snapshot.realized_pnl + snapshot.unrealized_pnl

    def return_percent(self, snapshot):
        if snapshot.cash == 0:
            return 0.0

        return (self.total_pnl(snapshot) / snapshot.cash) * 100

    def cash_ratio(self, snapshot):
        if snapshot.equity == 0:
            return 0.0

        return (snapshot.cash / snapshot.equity) * 100

    # --------------------------------------------------
    # Equity Metrics
    # --------------------------------------------------

    def equity_change(self, snapshot):
        return snapshot.equity - snapshot.cash

    def equity_gain(self, snapshot):
        return max(0, self.equity_change(snapshot))

    # --------------------------------------------------
    # Portfolio Health
    # --------------------------------------------------

    def is_growing(self, snapshot):
        return self.equity_change(snapshot) > 0

    def is_in_drawdown(self, snapshot):
        return self.equity_change(snapshot) < 0

    # --------------------------------------------------
    # Exposure
    # --------------------------------------------------

    def position_exposure(self, snapshot):
        return snapshot.open_positions

    def cash_utilization(self, snapshot):
        if snapshot.equity == 0:
            return 0.0

        return ((snapshot.equity - snapshot.cash) / snapshot.equity) * 100

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self, snapshot):
        return {
            "total_pnl": self.total_pnl(snapshot),
            "return_percent": self.return_percent(snapshot),
            "cash_ratio": self.cash_ratio(snapshot),
            "equity_change": self.equity_change(snapshot),
            "is_profitable": snapshot.is_profitable(),
            "has_open_positions": snapshot.has_open_positions(),
            "position_count": snapshot.open_positions,
            "cash": snapshot.cash,
        }
