import pytest

from execution.order_status import OrderStatus


@pytest.mark.parametrize(
    "terminal_state",
    [
        "FILLED",
        "CANCELLED",
        "REJECTED",
    ],
)
@pytest.mark.parametrize(
    "transition",
    [
        "mark_submitted",
        "mark_filled",
        "mark_cancelled",
        "mark_rejected",
    ],
)
def test_terminal_states_reject_all_transitions(
    terminal_state,
    transition,
):
    status = OrderStatus(state=terminal_state)

    with pytest.raises(
        ValueError,
        match=f"Invalid transition from {terminal_state}",
    ):
        getattr(status, transition)()


def test_create_order_status():
    status = OrderStatus()

    assert status.state == "NEW"


def test_mark_submitted():
    status = OrderStatus()

    status.mark_submitted()

    assert status.state == "SUBMITTED"


def test_mark_filled():
    status = OrderStatus()

    status.mark_filled()

    assert status.state == "FILLED"


def test_mark_cancelled():
    status = OrderStatus()

    status.mark_cancelled()

    assert status.state == "CANCELLED"


def test_mark_rejected():
    status = OrderStatus()

    status.mark_rejected()

    assert status.state == "REJECTED"


def test_is_open_new():
    status = OrderStatus()

    assert status.is_open() is True


def test_is_open_submitted():
    status = OrderStatus()

    status.mark_submitted()

    assert status.is_open() is True


def test_is_open_filled():
    status = OrderStatus()

    status.mark_filled()

    assert status.is_open() is False


def test_is_closed():
    status = OrderStatus()

    status.mark_filled()

    assert status.is_closed() is True


def test_is_closed_false_for_new():
    status = OrderStatus()

    assert status.is_closed() is False


def test_is_cancelled():
    status = OrderStatus()

    status.mark_cancelled()

    assert status.is_cancelled() is True


def test_is_cancelled_false_for_new():
    status = OrderStatus()

    assert status.is_cancelled() is False


def test_is_rejected():
    status = OrderStatus()

    status.mark_rejected()

    assert status.is_rejected() is True


def test_is_rejected_false_for_new():
    status = OrderStatus()

    assert status.is_rejected() is False


def test_to_dict():
    status = OrderStatus()

    assert status.to_dict() == {
        "state": "NEW",
    }


def test_string():
    status = OrderStatus()

    assert str(status) == "NEW"


def test_repr():
    status = OrderStatus()

    assert repr(status) == "OrderStatus(state='NEW')"


def test_reset():
    status = OrderStatus()

    status.mark_filled()
    status.reset()

    assert status.state == "NEW"
