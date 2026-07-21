from dataclasses import dataclass


@dataclass
class Exposure:
    max_exposure: float

    def within_limit(self, current_exposure: float) -> bool:
        return current_exposure <= self.max_exposure