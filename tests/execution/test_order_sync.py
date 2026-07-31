from unittest.mock import Mock

from execution.order_sync import OrderSync


class DummyOrder:
    def __init__(self):
        self.order_id = 101
        self.status = "FILLED"
        self.broker_order_id = "DH123"


def test_synchronize_orders():
    broker = Mock()
    broker.get_orders.return_value = [DummyOrder()]

    execution_sync = Mock()
    position_sync = Mock()

    sync = OrderSync(
        broker,
        execution_sync,
        position_sync,
    )

    sync.synchronize_orders()

    execution_sync.process.assert_called_once_with(
        order_id=101,
        status="FILLED",
        broker_order_id="DH123",
    )


def test_synchronize_positions():
    broker = Mock()
    execution_sync = Mock()
    position_sync = Mock()

    sync = OrderSync(
        broker,
        execution_sync,
        position_sync,
    )

    sync.synchronize_positions()

    position_sync.synchronize.assert_called_once()


def test_synchronize():
    broker = Mock()
    broker.get_orders.return_value = [DummyOrder()]

    execution_sync = Mock()
    position_sync = Mock()

    sync = OrderSync(
        broker,
        execution_sync,
        position_sync,
    )

    sync.synchronize()

    execution_sync.process.assert_called_once()
    position_sync.synchronize.assert_called_once()
