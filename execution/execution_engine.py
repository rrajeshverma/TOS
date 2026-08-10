"""
=========================================================
Trading Operating System (TOS)

Module      : Execution Engine
Description : Executes validated execution requests.
=========================================================
"""

from __future__ import annotations

from execution.execution_result import ExecutionResult
from execution.order_service_protocol import (
    OrderServiceProtocol,
)


class ExecutionEngine:
    def __init__(
        self,
        order_service: OrderServiceProtocol,
        execution_guard=None,
    ) -> None:
        self.order_service = order_service
        self.execution_guard = execution_guard

    def execute(
        self,
        request,
    ):
        if request is None:
            raise ValueError("ExecutionRequest cannot be None")

        try:
            if self.execution_guard is not None and not self.execution_guard.can_execute():
                return ExecutionResult(
                    success=False,
                    error="Execution blocked by safety guard",
                )

            order_id = self.order_service.submit(request)

            if hasattr(
                self.order_service,
                "place_order",
            ):
                response = self._place_order(request)

                broker_order_id = response.get("orderId")

                if broker_order_id and hasattr(
                    self.order_service,
                    "register_broker_order",
                ):
                    self.order_service.register_broker_order(
                        order_id,
                        broker_order_id,
                    )

                if hasattr(
                    self.order_service,
                    "update_status",
                ):
                    from execution.order_service import OrderStatus

                    self.order_service.update_status(
                        order_id,
                        OrderStatus.SUBMITTED,
                    )

            return ExecutionResult(
                success=True,
                order_id=order_id,
            )

        except Exception as exc:
            return ExecutionResult(
                success=False,
                error=str(exc),
            )

    def _place_order(
        self,
        request,
    ):
        return self.order_service.place_order(request)
