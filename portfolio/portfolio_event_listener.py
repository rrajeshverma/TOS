from __future__ import annotations

from execution.order_events import (
    OrderEvent,
    OrderEventType,
)


class PortfolioEventListener:
    """
    Updates the portfolio when execution events are received.
    """

    def __init__(
        self,
        portfolio_service,
    ) -> None:
        self._portfolio_service = portfolio_service

    def __call__(
        self,
        event: OrderEvent,
    ) -> None:
        if event.event_type == OrderEventType.FILLED:
            self._portfolio_service.on_order_filled(
                event.order_id,
                broker_order_id=event.broker_order_id,
            )

        elif event.event_type == OrderEventType.PARTIALLY_FILLED:
            self._portfolio_service.on_order_partially_filled(
                event.order_id,
                broker_order_id=event.broker_order_id,
            )

        elif event.event_type == OrderEventType.CANCELLED:
            self._portfolio_service.on_order_cancelled(
                event.order_id,
                broker_order_id=event.broker_order_id,
            )
