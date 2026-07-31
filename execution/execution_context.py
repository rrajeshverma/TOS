from dataclasses import dataclass

from domain.risk import Risk


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    risk: Risk
    quantity: int
