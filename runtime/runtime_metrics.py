"""
Runtime metrics.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeMetrics:
    """Tracks runtime operational metrics."""

    orders_submitted: int = 0
    orders_rejected: int = 0
    guard_blocks: int = 0
    reconnects: int = 0

    def increment_orders_submitted(self) -> None:
        self.orders_submitted += 1

    def increment_orders_rejected(self) -> None:
        self.orders_rejected += 1

    def increment_guard_blocks(self) -> None:
        self.guard_blocks += 1

    def increment_reconnects(self) -> None:
        self.reconnects += 1

    def snapshot(self) -> dict[str, int]:
        """Return a snapshot of runtime metrics."""

        return {
            "orders_submitted": self.orders_submitted,
            "orders_rejected": self.orders_rejected,
            "guard_blocks": self.guard_blocks,
            "reconnects": self.reconnects,
        }
