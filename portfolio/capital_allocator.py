class CapitalAllocator:
    def __init__(self, capital):
        self.capital = capital
        self.reserved = 0

    # --------------------------------------------------
    # Allocation
    # --------------------------------------------------

    def allocate(self, amount):
        return min(max(amount, 0), self.capital)

    def allocate_percent(self, percent):
        return (self.capital * percent) / 100

    # --------------------------------------------------
    # Reservation
    # --------------------------------------------------

    def reserve(self, amount):
        self.reserved = min(max(amount, 0), self.capital)

    def release(self, amount):
        self.reserved = max(0, self.reserved - amount)

    def available(self):
        return self.capital - self.reserved

    # --------------------------------------------------
    # Utilization
    # --------------------------------------------------

    def utilization_percent(self):
        if self.capital == 0:
            return 0.0
        return (self.reserved / self.capital) * 100

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):
        return {
            "capital": self.capital,
            "reserved": self.reserved,
            "available": self.available(),
            "utilization_percent": self.utilization_percent(),
        }
