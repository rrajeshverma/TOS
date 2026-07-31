"""
Tests:
Live Position Synchronization Flow

Flow:

Broker Filled Order
        |
        ▼
Position Synchronizer
        |
        ▼
Local Position State
"""

from execution.position_synchronizer import PositionSynchronizer


class DummyBroker:
    def __init__(self):
        self.positions = [
            {
                "symbol": "NIFTY",
                "quantity": 65,
                "side": "BUY",
            }
        ]

    def get_positions(self):
        return self.positions


def test_position_sync_fetches_broker_positions():
    broker = DummyBroker()

    synchronizer = PositionSynchronizer(broker)

    positions = synchronizer.sync()

    assert positions is not None


def test_position_sync_contains_symbol():
    broker = DummyBroker()

    synchronizer = PositionSynchronizer(broker)

    positions = synchronizer.sync()

    assert positions[0]["symbol"] == "NIFTY"


def test_position_sync_contains_quantity():
    broker = DummyBroker()

    synchronizer = PositionSynchronizer(broker)

    positions = synchronizer.sync()

    assert positions[0]["quantity"] == 65


def test_position_sync_handles_empty_positions():
    class EmptyBroker:
        def get_positions(self):
            return []

    synchronizer = PositionSynchronizer(EmptyBroker())

    positions = synchronizer.sync()

    assert positions == []
