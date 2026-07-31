from __future__ import annotations

from execution.order_events import (
    OrderEvent,
    OrderEventType,
)


class ExecutionService:
    """
    Coordinates the complete execution workflow.

    Responsibilities:
    - Obtain approval
    - Execute the trade
    - Track execution
    - Publish execution events
    """

    def __init__(
        self,
        approval_engine,
        execution_engine,
        execution_tracker,
        event_dispatcher,
    ) -> None:
        self._approval_engine = approval_engine
        self._execution_engine = execution_engine
        self._execution_tracker = execution_tracker
        self._event_dispatcher = event_dispatcher

    def execute(
        self,
        trade_request,
        risk_decision=None,
    ):
        approval = self._approval_engine.approve(
            trade_request,
            risk_decision,
        )

        if not approval.approved:
            return approval

        result = self._execution_engine.execute(
            trade_request,
        )

        if not getattr(result, "success", False):
            return result

        order_id = result.order_id

        self._execution_tracker.create(order_id)
        self._execution_tracker.submit(order_id)

        self._event_dispatcher.publish(
            OrderEvent(
                order_id=order_id,
                event_type=OrderEventType.SUBMITTED,
            )
        )

        return result
