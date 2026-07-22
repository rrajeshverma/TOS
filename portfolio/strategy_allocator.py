class StrategyAllocator:
    """
    Allocates portfolio capital among trading strategies.
    """

    def __init__(self, total_capital):
        self.total_capital = total_capital
        self.allocations = {}


    def allocate(self, strategy, amount):

        if amount < 0:
            amount = 0

        available = self.remaining_capital()

        amount = min(
            amount,
            available,
        )

        self.allocations[strategy] = amount

        return amount


    def get_allocation(self, strategy):

        return self.allocations.get(strategy, 0)


    def total_allocated(self):

        return sum(
            self.allocations.values()
        )


    def remaining_capital(self):

        return max(
            0,
            self.total_capital - self.total_allocated()
        )


    def release(self, strategy):

        return self.allocations.pop(
            strategy,
            0,
        )


    def utilization(self):

        if self.total_capital == 0:
            return 0.0

        return (
            self.total_allocated()
            / self.total_capital
        ) * 100


    def summary(self):

        return {
            "total_capital": self.total_capital,
            "allocated": self.total_allocated(),
            "remaining": self.remaining_capital(),
            "utilization": self.utilization(),
            "strategies": len(self.allocations),
        }
