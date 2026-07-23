class RiskAllocator:
    """
    Controls risk allocation across strategies.
    """

    def __init__(self, total_risk):
        self.total_risk = total_risk
        self.allocations = {}
        self.daily_loss = 0

    def max_strategy_risk(self, strategy):
        return self.allocations.get(strategy, 0)

    def allocate_risk(self, strategy, amount):
        if amount < 0:
            amount = 0

        available = self.remaining_risk()

        amount = min(amount, available)

        self.allocations[strategy] = amount

        return amount

    def total_allocated_risk(self):
        return sum(self.allocations.values())

    def remaining_risk(self):
        return max(0, self.total_risk - self.total_allocated_risk())

    def distribute_daily_loss(self, amount):
        self.daily_loss = max(0, amount)

        return self.daily_loss

    def validate_margin(self, required):
        return required <= self.remaining_risk()

    def summary(self):
        return {
            "total_risk": self.total_risk,
            "allocated_risk": self.total_allocated_risk(),
            "remaining_risk": self.remaining_risk(),
            "daily_loss": self.daily_loss,
            "strategies": len(self.allocations),
        }
