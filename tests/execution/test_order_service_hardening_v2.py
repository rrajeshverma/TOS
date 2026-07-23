import pytest

from execution.order_service import OrderService, OrderStatus


def make_order(quantity=10):
    return {
        "symbol": "NIFTY",
        "quantity": quantity,
    }


def test_filled_quantity_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.filled_quantity(999)


def test_remaining_quantity_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.remaining_quantity(999)


def test_average_fill_price_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.average_fill_price(999)


def test_order_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.order(999)


def test_modify_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.modify_order(999, quantity=5)


@pytest.mark.parametrize("quantity", [0, -1, -100])
def test_modify_invalid_quantity(quantity):
    service = OrderService()

    order_id = service.submit(make_order())

    with pytest.raises(ValueError):
        service.modify_order(order_id, quantity=quantity)


def test_modify_less_than_filled_quantity():
    service = OrderService()

    order_id = service.submit(make_order(quantity=20))

    service.record_fill(order_id, 10, 100)

    with pytest.raises(ValueError):
        service.modify_order(order_id, quantity=5)


def test_record_fill_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.record_fill(999, 5, 100)


def test_record_fill_overfill():
    service = OrderService()

    order_id = service.submit(make_order(quantity=10))

    with pytest.raises(ValueError):
        service.record_fill(order_id, 11, 100)


def test_update_status_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.update_status(999, OrderStatus.SUBMITTED)


def test_register_broker_order_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.register_broker_order(999, "BROKER-1")


def test_register_broker_order_twice():
    service = OrderService()

    order_id = service.submit(make_order())

    service.register_broker_order(order_id, "ABC123")

    with pytest.raises(ValueError):
        service.register_broker_order(order_id, "XYZ456")


def test_process_unknown_broker_callback():
    service = OrderService()

    with pytest.raises(KeyError):
        service.process_broker_callback(
            "UNKNOWN",
            OrderStatus.SUBMITTED,
        )


def test_average_fill_price_zero_before_fill():
    service = OrderService()

    order_id = service.submit(make_order())

    assert service.average_fill_price(order_id) == 0.0


def test_remaining_quantity_after_partial_fill():
    service = OrderService()

    order_id = service.submit(make_order(quantity=20))

    service.record_fill(order_id, 8, 100)

    assert service.remaining_quantity(order_id) == 12


def test_filled_quantity_after_multiple_fills():
    service = OrderService()

    order_id = service.submit(make_order(quantity=20))

    service.record_fill(order_id, 5, 100)
    service.record_fill(order_id, 10, 120)

    assert service.filled_quantity(order_id) == 15


def test_average_fill_price_weighted():
    service = OrderService()

    order_id = service.submit(make_order(quantity=20))

    service.record_fill(order_id, 5, 100)
    service.record_fill(order_id, 15, 200)

    expected = (5 * 100 + 15 * 200) / 20

    assert service.average_fill_price(order_id) == expected


def test_order_returns_copy():
    service = OrderService()

    order_id = service.submit(make_order())

    order = service.order(order_id)

    order["quantity"] = 999

    assert service.order(order_id)["quantity"] == 10


def test_get_returns_original_data():
    service = OrderService()

    order = make_order()

    order_id = service.submit(order)

    assert service.get(order_id) == order


def test_order_count_after_multiple_submissions():
    service = OrderService()

    for _ in range(5):
        service.submit(make_order())

    assert service.order_count == 5
