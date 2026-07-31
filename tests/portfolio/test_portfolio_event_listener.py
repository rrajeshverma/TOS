from unittest.mock import Mock

from execution.order_events import (
    OrderEvent,
    OrderEventType,
)
from portfolio.portfolio_event_listener import (
    PortfolioEventListener,
)


def create_listener():
    service = Mock()

    return (
        PortfolioEventListener(service),
        service,
    )


def test_filled_event():
    listener, service = create_listener()

    listener(
        OrderEvent(
            order_id=1,
            event_type=OrderEventType.FILLED,
            broker_order_id="DHAN-1",
        )
    )

    service.on_order_filled.assert_called_once_with(
        1,
        broker_order_id="DHAN-1",
    )


def test_partial_fill_event():
    listener, service = create_listener()

    listener(
        OrderEvent(
            order_id=2,
            event_type=OrderEventType.PARTIALLY_FILLED,
            broker_order_id="DHAN-2",
        )
    )

    service.on_order_partially_filled.assert_called_once_with(
        2,
        broker_order_id="DHAN-2",
    )


def test_cancelled_event():
    listener, service = create_listener()

    listener(
        OrderEvent(
            order_id=3,
            event_type=OrderEventType.CANCELLED,
            broker_order_id="DHAN-3",
        )
    )

    service.on_order_cancelled.assert_called_once_with(
        3,
        broker_order_id="DHAN-3",
    )


def test_submitted_event_ignored():
    listener, service = create_listener()

    listener(
        OrderEvent(
            order_id=4,
            event_type=OrderEventType.SUBMITTED,
        )
    )

    service.on_order_filled.assert_not_called()
    service.on_order_partially_filled.assert_not_called()
    service.on_order_cancelled.assert_not_called()


def test_pending_event_ignored():
    listener, service = create_listener()

    listener(
        OrderEvent(
            order_id=5,
            event_type=OrderEventType.PENDING,
        )
    )

    service.on_order_filled.assert_not_called()
    service.on_order_partially_filled.assert_not_called()
    service.on_order_cancelled.assert_not_called()
