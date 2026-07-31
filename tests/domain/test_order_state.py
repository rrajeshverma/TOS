import pytest

from domain.order_state import OrderState


def test_new_state():
    assert OrderState.NEW.value == "NEW"


def test_submitted_state():
    assert OrderState.SUBMITTED.value == "SUBMITTED"


def test_acknowledged_state():
    assert OrderState.ACKNOWLEDGED.value == "ACKNOWLEDGED"


def test_partially_filled_state():
    assert OrderState.PARTIALLY_FILLED.value == "PARTIALLY_FILLED"


def test_filled_state():
    assert OrderState.FILLED.value == "FILLED"


def test_cancelled_state():
    assert OrderState.CANCELLED.value == "CANCELLED"


def test_rejected_state():
    assert OrderState.REJECTED.value == "REJECTED"


def test_expired_state():
    assert OrderState.EXPIRED.value == "EXPIRED"


def test_unique_values():
    values = {state.value for state in OrderState}

    assert len(values) == len(OrderState)


def test_enum_length():
    assert len(OrderState) == 8


@pytest.mark.parametrize(
    "state",
    [
        OrderState.NEW,
        OrderState.SUBMITTED,
        OrderState.ACKNOWLEDGED,
        OrderState.PARTIALLY_FILLED,
        OrderState.FILLED,
        OrderState.CANCELLED,
        OrderState.REJECTED,
        OrderState.EXPIRED,
    ],
)
def test_members_are_enum(state):
    assert isinstance(state, OrderState)
