"""
Execution Tracker

Tracks the execution lifecycle of orders.
"""

from __future__ import annotations

from typing import ClassVar

from execution.execution_status import ExecutionStatus


class ExecutionTracker:
    _VALID_TRANSITIONS: ClassVar[dict] = {
        ExecutionStatus.PENDING: {
            ExecutionStatus.SUBMITTED,
        },
        ExecutionStatus.SUBMITTED: {
            ExecutionStatus.ACCEPTED,
            ExecutionStatus.REJECTED,
            ExecutionStatus.CANCELLED,
            ExecutionStatus.EXPIRED,
        },
        ExecutionStatus.ACCEPTED: {
            ExecutionStatus.PARTIALLY_FILLED,
            ExecutionStatus.FILLED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.PARTIALLY_FILLED: {
            ExecutionStatus.PARTIALLY_FILLED,
            ExecutionStatus.FILLED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.FILLED: set(),
        ExecutionStatus.REJECTED: set(),
        ExecutionStatus.CANCELLED: set(),
        ExecutionStatus.EXPIRED: set(),
    }

    def __init__(self) -> None:
        self._orders: dict[str, dict] = {}

    def create(self, order_id: str) -> None:
        """
        Register a new order.
        """
        if order_id in self._orders:
            raise ValueError(f"Order '{order_id}' already exists.")

        self._orders[order_id] = {
            "status": ExecutionStatus.PENDING,
            "history": [
                ExecutionStatus.PENDING,
            ],
        }

    def transition(
        self,
        order_id: str,
        status: ExecutionStatus,
    ) -> None:
        """
        Move an order to a new execution status.
        """
        order = self._get_order(order_id)

        current = order["status"]

        if status not in self._VALID_TRANSITIONS[current]:
            raise ValueError(f"Invalid execution state transition: {current.name} -> {status.name}")

        order["status"] = status
        order["history"].append(status)

    def status(
        self,
        order_id: str,
    ) -> ExecutionStatus:
        """
        Return current execution status.
        """
        return self._get_order(order_id)["status"]

    def history(
        self,
        order_id: str,
    ) -> list[ExecutionStatus]:
        """
        Return execution history.
        """
        return list(self._get_order(order_id)["history"])

    def exists(
        self,
        order_id: str,
    ) -> bool:
        return order_id in self._orders

    def submit(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.SUBMITTED,
        )

    def accept(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.ACCEPTED,
        )

    def partial_fill(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.PARTIALLY_FILLED,
        )

    def fill(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.FILLED,
        )

    def reject(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.REJECTED,
        )

    def cancel(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.CANCELLED,
        )

    def expire(
        self,
        order_id: str,
    ) -> None:
        self.transition(
            order_id,
            ExecutionStatus.EXPIRED,
        )

    def _get_order(
        self,
        order_id: str,
    ) -> dict:
        if order_id not in self._orders:
            raise ValueError(f"Unknown order '{order_id}'.")

        return self._orders[order_id]
