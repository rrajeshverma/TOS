"""
Order Event

Represents an immutable execution event.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from execution.execution_status import ExecutionStatus


@dataclass(frozen=True, slots=True)
class OrderEvent:
    """
    Immutable execution event.
    """

    order_id: str

    status: ExecutionStatus

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    broker_order_id: str | None = None

    message: str = ""

    quantity: int | None = None

    price: float | None = None
