from unittest.mock import Mock

from execution.position_synchronizer import PositionSynchronizer


def test_sync_positions_calls_broker():
    broker = Mock()
    broker.get_positions.return_value = []

    synchronizer = PositionSynchronizer(broker)

    result = synchronizer.sync()

    broker.get_positions.assert_called_once()
    assert result == []
