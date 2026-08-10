from dataclasses import dataclass


@dataclass
class ExecutionResult:
    order_id: str
    status: str
    filled_qty: int
    avg_price: float
    message: str | None = None
