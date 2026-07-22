import pytest

from execution.order_status import OrderStatus


def test_filled_order_cannot_move_back():

    status = OrderStatus()

    status.mark_filled()

    with pytest.raises(ValueError):
        status.mark_submitted()



def test_cancelled_order_cannot_move_back():

    status = OrderStatus()

    status.mark_cancelled()

    with pytest.raises(ValueError):
        status.mark_submitted()



def test_rejected_order_cannot_move_back():

    status = OrderStatus()

    status.mark_rejected()

    with pytest.raises(ValueError):
        status.mark_filled()
