import pytest

from brokers.base_broker import BaseBroker


def test_base_broker_is_abstract():
    with pytest.raises(TypeError):
        BaseBroker()


class DummyBroker(BaseBroker):
    pass


def test_incomplete_broker_cannot_be_created():
    with pytest.raises(TypeError):
        DummyBroker()


class ConcreteBroker(BaseBroker):
    connect = BaseBroker.connect
    disconnect = BaseBroker.disconnect
    is_connected = BaseBroker.is_connected
    place_order = BaseBroker.place_order
    modify_order = BaseBroker.modify_order
    cancel_order = BaseBroker.cancel_order
    get_order = BaseBroker.get_order
    get_orders = BaseBroker.get_orders
    get_positions = BaseBroker.get_positions
    get_holdings = BaseBroker.get_holdings
    get_funds = BaseBroker.get_funds


# Bypass ABC checks so we can execute the default implementations
ConcreteBroker.__abstractmethods__ = frozenset()


@pytest.fixture
def broker():
    return ConcreteBroker()


def test_connect_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.connect()


def test_disconnect_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.disconnect()


def test_is_connected_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.is_connected()


def test_place_order_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.place_order(None)


def test_modify_order_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.modify_order("1", 1)


def test_cancel_order_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.cancel_order("1")


def test_get_order_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.get_order("1")


def test_get_orders_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.get_orders()


def test_get_positions_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.get_positions()


def test_get_holdings_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.get_holdings()


def test_get_funds_not_implemented(broker):
    with pytest.raises(NotImplementedError):
        broker.get_funds()
