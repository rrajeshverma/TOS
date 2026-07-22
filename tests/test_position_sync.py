from portfolio.position_sync import PositionSync


def test_create_position_sync():
    sync = PositionSync()

    assert sync.local_positions == {}
    assert sync.broker_positions == {}


def test_set_local_position():
    sync = PositionSync()

    sync.set_local("NIFTY", 2)

    assert sync.local_positions["NIFTY"] == 2


def test_set_broker_position():
    sync = PositionSync()

    sync.set_broker("NIFTY", 2)

    assert sync.broker_positions["NIFTY"] == 2


def test_positions_match():
    sync = PositionSync()

    sync.set_local("NIFTY", 2)
    sync.set_broker("NIFTY", 2)

    assert sync.is_in_sync() is True


def test_positions_do_not_match():
    sync = PositionSync()

    sync.set_local("NIFTY", 2)
    sync.set_broker("NIFTY", 1)

    assert sync.is_in_sync() is False


def test_difference():
    sync = PositionSync()

    sync.set_local("NIFTY", 3)
    sync.set_broker("NIFTY", 1)

    assert sync.difference("NIFTY") == 2


def test_missing_symbol():
    sync = PositionSync()

    assert sync.difference("BANKNIFTY") == 0


def test_reset():
    sync = PositionSync()

    sync.set_local("NIFTY", 2)
    sync.set_broker("NIFTY", 2)

    sync.reset()

    assert sync.local_positions == {}
    assert sync.broker_positions == {}


def test_summary():
    sync = PositionSync()

    sync.set_local("NIFTY", 2)
    sync.set_broker("NIFTY", 2)

    summary = sync.summary()

    assert summary["in_sync"] is True


def test_summary_contains_positions():
    sync = PositionSync()

    summary = sync.summary()

    assert "local_positions" in summary
    assert "broker_positions" in summary


def test_multiple_symbols():
    sync = PositionSync()

    sync.set_local("NIFTY", 1)
    sync.set_local("BANKNIFTY", 2)

    sync.set_broker("NIFTY", 1)
    sync.set_broker("BANKNIFTY", 2)

    assert sync.is_in_sync() is True


def test_difference_negative():
    sync = PositionSync()

    sync.set_local("NIFTY", 1)
    sync.set_broker("NIFTY", 3)

    assert sync.difference("NIFTY") == -2


def test_update_existing_position():
    sync = PositionSync()

    sync.set_local("NIFTY", 1)
    sync.set_local("NIFTY", 5)

    assert sync.local_positions["NIFTY"] == 5


def test_remove_position():
    sync = PositionSync()

    sync.set_local("NIFTY", 2)

    sync.remove_local("NIFTY")

    assert "NIFTY" not in sync.local_positions


def test_remove_broker_position():
    sync = PositionSync()

    sync.set_broker("NIFTY", 2)

    sync.remove_broker("NIFTY")

    assert "NIFTY" not in sync.broker_positions
