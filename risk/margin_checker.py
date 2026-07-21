from dataclasses import dataclass


@dataclass
class MarginChecker:
    available_margin: float

    def has_sufficient_margin(self, required_margin: float) -> bool:
        return self.available_margin >= required_margin