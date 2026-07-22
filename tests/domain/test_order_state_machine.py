import pytest

from domain.order_state import OrderState
from domain.order_state_machine import OrderStateMachine


def test_initial_state():
    machine = OrderStateMachine()

    assert machine.state == OrderState.NEW


def test_new_to_submitted():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)

    assert machine.state == OrderState.SUBMITTED


def test_submitted_to_acknowledged():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.ACKNOWLEDGED)

    assert machine.state == OrderState.ACKNOWLEDGED


def test_ack_to_partial():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.ACKNOWLEDGED)
    machine.transition(OrderState.PARTIALLY_FILLED)

    assert machine.state == OrderState.PARTIALLY_FILLED


def test_partial_to_filled():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.ACKNOWLEDGED)
    machine.transition(OrderState.PARTIALLY_FILLED)
    machine.transition(OrderState.FILLED)

    assert machine.state == OrderState.FILLED


def test_ack_to_cancelled():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.ACKNOWLEDGED)
    machine.transition(OrderState.CANCELLED)

    assert machine.state == OrderState.CANCELLED


def test_submitted_to_rejected():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.REJECTED)

    assert machine.state == OrderState.REJECTED


def test_submitted_to_expired():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.EXPIRED)

    assert machine.state == OrderState.EXPIRED


@pytest.mark.parametrize(
    "target",
    [
        OrderState.NEW,
        OrderState.PARTIALLY_FILLED,
        OrderState.FILLED,
        OrderState.CANCELLED,
    ],
)
def test_invalid_from_new(target):
    machine = OrderStateMachine()

    with pytest.raises(ValueError):
        machine.transition(target)


def test_filled_terminal():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.ACKNOWLEDGED)
    machine.transition(OrderState.PARTIALLY_FILLED)
    machine.transition(OrderState.FILLED)

    with pytest.raises(ValueError):
        machine.transition(OrderState.CANCELLED)


def test_rejected_terminal():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.REJECTED)

    with pytest.raises(ValueError):
        machine.transition(OrderState.FILLED)


def test_cancelled_terminal():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.ACKNOWLEDGED)
    machine.transition(OrderState.CANCELLED)

    with pytest.raises(ValueError):
        machine.transition(OrderState.FILLED)


def test_expired_terminal():
    machine = OrderStateMachine()

    machine.transition(OrderState.SUBMITTED)
    machine.transition(OrderState.EXPIRED)

    with pytest.raises(ValueError):
        machine.transition(OrderState.FILLED)