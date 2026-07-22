from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionRequest:
    symbol: str
    side: str
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if self.side not in ("BUY", "SELL"):
            raise ValueError("Invalid side")
