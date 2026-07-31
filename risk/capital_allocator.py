from dataclasses import dataclass


@dataclass
class CapitalAllocator:
    capital: float

    def allocate(self, amount: float) -> bool:
        if amount > self.capital:
            return False

        self.capital -= amount
        return True
