from unittest.mock import Mock

from portfolio.position_sync import PositionSync


def test_sync_positions_from_broker():
    broker = Mock()

    broker.get_positions.return_value = [
        {
            "securityId": "12345",
            "quantity": 50,
        },
        {
            "securityId": "67890",
            "quantity": 25,
        },
    ]

    sync = PositionSync(broker)

    positions = sync.sync()

    broker.get_positions.assert_called_once_with()

    assert len(positions) == 2
    assert positions[0]["securityId"] == "12345"
