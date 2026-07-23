import pytest

from brokers.broker import Broker


def test_can_create_broker():
    assert Broker() is not None


def test_has_place_order():
    broker = Broker()

    assert hasattr(broker, "place_order")


def test_has_cancel_order():
    broker = Broker()

    assert hasattr(broker, "cancel_order")


def test_has_modify_order():
    broker = Broker()

    assert hasattr(broker, "modify_order")


def test_has_positions():
    broker = Broker()

    assert hasattr(broker, "positions")


def test_has_orders():
    broker = Broker()

    assert hasattr(broker, "orders")


def test_has_holdings():
    broker = Broker()

    assert hasattr(broker, "holdings")


def test_place_order_not_implemented():
    with pytest.raises(NotImplementedError):
        Broker().place_order({})


def test_cancel_order_not_implemented():
    with pytest.raises(NotImplementedError):
        Broker().cancel_order("1")


def test_modify_order_not_implemented():
    with pytest.raises(NotImplementedError):
        Broker().modify_order("1", {})


def test_positions_not_implemented():
    with pytest.raises(NotImplementedError):
        Broker().positions()


def test_orders_not_implemented():
    with pytest.raises(NotImplementedError):
        Broker().orders()


def test_holdings_not_implemented():
    with pytest.raises(NotImplementedError):
        Broker().holdings()


def test_repeatable():
    broker = Broker()

    assert isinstance(broker, Broker)


def test_stateless():
    broker = Broker()

    assert vars(broker) == {}


def test_place_order_exists():
    assert callable(Broker().place_order)


def test_cancel_exists():
    assert callable(Broker().cancel_order)


def test_modify_exists():
    assert callable(Broker().modify_order)


def test_positions_exists():
    assert callable(Broker().positions)


def test_orders_exists():
    assert callable(Broker().orders)
