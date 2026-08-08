from unittest.mock import Mock

from runtime.recovery_manager import RecoveryManager


def create_broker():
    broker = Mock()

    broker.get_orders.return_value = []
    broker.get_positions.return_value = []
    broker.get_holdings.return_value = []
    broker.get_funds.return_value = {}

    return broker


def test_recovery_returns_state():
    broker = create_broker()

    manager = RecoveryManager(broker)

    state = manager.recover()

    assert state == {
        "orders": [],
        "positions": [],
        "holdings": [],
        "funds": {},
    }


def test_recovery_calls_get_orders():
    broker = create_broker()

    RecoveryManager(broker).recover()

    broker.get_orders.assert_called_once_with()


def test_recovery_calls_get_positions():
    broker = create_broker()

    RecoveryManager(broker).recover()

    broker.get_positions.assert_called_once_with()


def test_recovery_calls_get_holdings():
    broker = create_broker()

    RecoveryManager(broker).recover()

    broker.get_holdings.assert_called_once_with()


def test_recovery_calls_get_funds():
    broker = create_broker()

    RecoveryManager(broker).recover()

    broker.get_funds.assert_called_once_with()
