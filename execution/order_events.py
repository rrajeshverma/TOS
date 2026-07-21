from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OrderEventType(str, Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, slots=True)
class OrderEvent:
    order_id: int
    event_type: OrderEventType
    broker_order_id: str | None = None