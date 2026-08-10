from dataclasses import dataclass


@dataclass
class ExecutionResult:
    success: bool
    order_id: str | None = None
    message: str | None = None
    error: str | None = None  # ✅ ADD THIS
    filled_qty: int = 0
    avg_price: float = 0.0
