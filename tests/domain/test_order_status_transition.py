import pytest

from domain.order_status_transition import OrderStatusTransition
from shared.enums import OrderStatus


@pytest.mark.parametrize(
    "current,target",
    [
        (OrderStatus.CREATED, OrderStatus.PENDING),
        (OrderStatus.PENDING, OrderStatus.EXECUTED),
        (OrderStatus.PENDING, OrderStatus.REJECTED),
        (OrderStatus.PENDING, OrderStatus.CANCELLED),
    ],
)
def test_valid_transition(current, target):
    assert OrderStatusTransition.can_transition(
        current,
        target,
    )


@pytest.mark.parametrize(
    "current,target",
    [
        (OrderStatus.CREATED, OrderStatus.EXECUTED),
        (OrderStatus.CREATED, OrderStatus.REJECTED),
        (OrderStatus.CREATED, OrderStatus.CANCELLED),
        (OrderStatus.EXECUTED, OrderStatus.PENDING),
        (OrderStatus.EXECUTED, OrderStatus.CREATED),
        (OrderStatus.REJECTED, OrderStatus.EXECUTED),
        (OrderStatus.CANCELLED, OrderStatus.EXECUTED),
    ],
)
def test_invalid_transition(current, target):
    assert not OrderStatusTransition.can_transition(
        current,
        target,
    )


def test_terminal_executed():
    assert not OrderStatusTransition.can_transition(
        OrderStatus.EXECUTED,
        OrderStatus.PENDING,
    )


def test_terminal_rejected():
    assert not OrderStatusTransition.can_transition(
        OrderStatus.REJECTED,
        OrderStatus.PENDING,
    )


def test_terminal_cancelled():
    assert not OrderStatusTransition.can_transition(
        OrderStatus.CANCELLED,
        OrderStatus.PENDING,
    )
