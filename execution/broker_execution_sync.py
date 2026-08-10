from __future__ import annotations

from typing import ClassVar

from execution.execution_status import ExecutionStatus
from execution.order_events import (
    OrderEvent,
    OrderEventType,
)


class BrokerExecutionSync:
    _EVENT_TYPES: ClassVar[dict] = {
        ExecutionStatus.SUBMITTED: OrderEventType.SUBMITTED,
        ExecutionStatus.PARTIALLY_FILLED: OrderEventType.PARTIALLY_FILLED,
        ExecutionStatus.FILLED: OrderEventType.FILLED,
        ExecutionStatus.CANCELLED: OrderEventType.CANCELLED,
    }

    def __init__(
        self,
        tracker,
        dispatcher,
    ) -> None:
        self._tracker = tracker
        self._dispatcher = dispatcher

    def process(
        self,
        order_id: int,
        status: ExecutionStatus,
        broker_order_id: str | None = None,
    ) -> None:
        if status == ExecutionStatus.SUBMITTED:
            self._tracker.submit(order_id)

        elif status == ExecutionStatus.PARTIALLY_FILLED:
            self._tracker.partial_fill(order_id)

        elif status == ExecutionStatus.FILLED:
            self._tracker.fill(order_id)

        elif status == ExecutionStatus.CANCELLED:
            self._tracker.cancel(order_id)

        else:
            return

        self._dispatcher.publish(
            OrderEvent(
                order_id=order_id,
                event_type=self._EVENT_TYPES[status],
                broker_order_id=broker_order_id,
            )
        )
