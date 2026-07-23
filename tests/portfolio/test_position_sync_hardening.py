from portfolio.position_sync import PositionSync


def test_missing_broker_positions():
    sync = PositionSync()

    sync.set_local(
        "NIFTY",
        65,
    )

    assert sync.missing_broker_positions() == ["NIFTY"]


def test_extra_broker_positions():
    sync = PositionSync()

    sync.set_broker(
        "BANKNIFTY",
        25,
    )

    assert sync.extra_broker_positions() == ["BANKNIFTY"]


def test_sync_report():
    sync = PositionSync()

    sync.set_local(
        "NIFTY",
        65,
    )

    sync.set_broker(
        "NIFTY",
        60,
    )

    report = sync.sync_report()

    assert report["in_sync"] is False
    assert report["differences"]["NIFTY"] == 5
