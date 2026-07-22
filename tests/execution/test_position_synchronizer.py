from execution.position_synchronizer import PositionSynchronizer


def test_position_sync_calls_broker():

    class Broker:

        def __init__(self):
            self.called = False

        def get_positions(self):
            self.called = True
            return []

    broker = Broker()

    sync = PositionSynchronizer(
        broker
    )

    sync.sync()

    assert broker.called is True


def test_position_sync_returns_positions():

    class Broker:

        def get_positions(self):
            return [
                {
                    "symbol": "NIFTY",
                    "quantity": 65,
                }
            ]

    result = PositionSynchronizer(
        Broker()
    ).sync()

    assert len(result) == 1


def test_position_sync_empty_positions():

    class Broker:

        def get_positions(self):
            return []

    result = PositionSynchronizer(
        Broker()
    ).sync()

    assert result == []


def test_position_sync_preserves_broker_data():

    positions = [
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    ]

    class Broker:

        def get_positions(self):
            return positions

    result = PositionSynchronizer(
        Broker()
    ).sync()

    assert result == positions


def test_position_sync_broker_exception():

    import pytest

    class Broker:

        def get_positions(self):
            raise Exception(
                "Broker unavailable"
            )

    with pytest.raises(Exception):
        PositionSynchronizer(
            Broker()
        ).sync()


def test_position_sync_multiple_calls():

    class Broker:

        def __init__(self):
            self.count = 0

        def get_positions(self):
            self.count += 1
            return []

    broker = Broker()

    sync = PositionSynchronizer(
        broker
    )

    sync.sync()
    sync.sync()

    assert broker.count == 2


def test_position_sync_with_multiple_positions():

    class Broker:

        def get_positions(self):
            return [
                {"symbol": "NIFTY"},
                {"symbol": "BANKNIFTY"},
            ]

    result = PositionSynchronizer(
        Broker()
    ).sync()

    assert len(result) == 2


def test_position_sync_keeps_order():

    class Broker:

        def get_positions(self):
            return [
                {"symbol": "A"},
                {"symbol": "B"},
            ]

    result = PositionSynchronizer(
        Broker()
    ).sync()

    assert result[0]["symbol"] == "A"
    assert result[1]["symbol"] == "B"