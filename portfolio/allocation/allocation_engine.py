class AllocationEngine:
    def __init__(self, capital):
        self.capital = capital
        self.allocations = {}

    def allocate(self, strategy, amount):
        if amount < 0:
            amount = 0

        if amount > self.remaining_capital():
            amount = self.remaining_capital()

        self.allocations[strategy] = amount

        return amount

    def get_allocation(self, strategy):
        return self.allocations.get(strategy, 0)

    def total_allocated(self):
        return sum(self.allocations.values())

    def remaining_capital(self):
        return self.capital - self.total_allocated()

    def remove_allocation(self, strategy):
        self.allocations.pop(strategy, None)

    def summary(self):
        return {
            "capital": self.capital,
            "allocated": self.total_allocated(),
            "remaining": self.remaining_capital(),
            "strategies": len(self.allocations),
        }
