from unittest.mock import Mock

import pytest

from portfolio.position_sync import PositionSync


def test_create_position_sync():
    sync = PositionSync()

    assert sync.local_positions == {}
    assert sync.broker_positions == {}


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


# ---------------------------------------------------------
# Additional Certification Tests
# ---------------------------------------------------------


def test_starts_in_sync():
    sync = PositionSync()

    assert sync.is_in_sync()


def test_set_local_position():
    sync = PositionSync()

    sync.set_local("NIFTY", 50)

    assert sync.local_positions["NIFTY"] == 50


def test_set_broker_position():
    sync = PositionSync()

    sync.set_broker("NIFTY", 50)

    assert sync.broker_positions["NIFTY"] == 50


def test_difference_zero():
    sync = PositionSync()

    sync.set_local("NIFTY", 50)
    sync.set_broker("NIFTY", 50)

    assert sync.difference("NIFTY") == 0


def test_difference_positive():
    sync = PositionSync()

    sync.set_local("NIFTY", 75)
    sync.set_broker("NIFTY", 50)

    assert sync.difference("NIFTY") == 25


def test_difference_negative():
    sync = PositionSync()

    sync.set_local("NIFTY", 25)
    sync.set_broker("NIFTY", 50)

    assert sync.difference("NIFTY") == -25


def test_remove_local():
    sync = PositionSync()

    sync.set_local("NIFTY", 50)
    sync.remove_local("NIFTY")

    assert "NIFTY" not in sync.local_positions


def test_remove_broker():
    sync = PositionSync()

    sync.set_broker("NIFTY", 50)
    sync.remove_broker("NIFTY")

    assert "NIFTY" not in sync.broker_positions


def test_reset():
    sync = PositionSync()

    sync.set_local("NIFTY", 50)
    sync.set_broker("BANKNIFTY", 25)

    sync.reset()

    assert sync.local_positions == {}
    assert sync.broker_positions == {}


def test_summary_contains_expected_keys():
    sync = PositionSync()

    summary = sync.summary()

    assert set(summary) == {
        "local_positions",
        "broker_positions",
        "in_sync",
    }


def test_sync_without_broker_raises():
    sync = PositionSync()

    with pytest.raises(RuntimeError):
        sync.sync()


def test_sync_populates_broker_positions():
    broker = Mock()
    broker.get_positions.return_value = [
        {"securityId": "NIFTY", "quantity": 50},
        {"securityId": "BANKNIFTY", "quantity": 25},
    ]

    sync = PositionSync(broker=broker)

    sync.sync()

    assert sync.broker_positions == {
        "NIFTY": 50,
        "BANKNIFTY": 25,
    }


def test_missing_broker_positions():
    sync = PositionSync()

    sync.set_local("NIFTY", 50)

    assert sync.missing_broker_positions() == ["NIFTY"]


def test_extra_broker_positions():
    sync = PositionSync()

    sync.set_broker("NIFTY", 50)

    assert sync.extra_broker_positions() == ["NIFTY"]


def test_sync_report_contains_expected_keys():
    sync = PositionSync()

    report = sync.sync_report()

    assert set(report) == {
        "in_sync",
        "missing",
        "extra",
        "differences",
    }
