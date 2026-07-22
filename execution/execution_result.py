from dataclasses import dataclass


@dataclass
class ExecutionResult:
    success: bool
    order_id: str | None = None
    error: str | None = None
