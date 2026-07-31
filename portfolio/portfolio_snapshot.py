class PortfolioSnapshot:
    def __init__(
        self,
        cash,
        equity,
        realized_pnl,
        unrealized_pnl,
        open_positions,
    ):
        self.cash = cash
        self.equity = equity
        self.realized_pnl = realized_pnl
        self.unrealized_pnl = unrealized_pnl
        self.open_positions = open_positions

    def to_dict(self):
        return {
            "cash": self.cash,
            "equity": self.equity,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "open_positions": self.open_positions,
        }

    # -----------------------------
    # Portfolio Metrics
    # -----------------------------

    def total_pnl(self):
        return self.realized_pnl + self.unrealized_pnl

    def is_profitable(self):
        return self.total_pnl() > 0

    def is_flat(self):
        return self.open_positions == 0

    def has_open_positions(self):
        return self.open_positions > 0

    # -----------------------------
    # Position Management
    # -----------------------------

    def increment_positions(self):
        self.open_positions += 1

    def decrement_positions(self):
        if self.open_positions > 0:
            self.open_positions -= 1

    def reset_positions(self):
        self.open_positions = 0

    # -----------------------------
    # Cash Management
    # -----------------------------

    def deposit(self, amount):
        self.cash += amount

    def withdraw(self, amount):
        self.cash = max(0, self.cash - amount)

    # -----------------------------
    # Utilities
    # -----------------------------

    def copy(self):
        return PortfolioSnapshot(
            cash=self.cash,
            equity=self.equity,
            realized_pnl=self.realized_pnl,
            unrealized_pnl=self.unrealized_pnl,
            open_positions=self.open_positions,
        )
