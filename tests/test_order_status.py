from execution.order_status import OrderStatus


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


def test_is_cancelled():
    status = OrderStatus()

    status.mark_cancelled()

    assert status.is_cancelled() is True


def test_is_rejected():
    status = OrderStatus()

    status.mark_rejected()

    assert status.is_rejected() is True


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

    assert "NEW" in repr(status)


def test_reset():
    status = OrderStatus()

    status.mark_filled()
    status.reset()

    assert status.state == "NEW"