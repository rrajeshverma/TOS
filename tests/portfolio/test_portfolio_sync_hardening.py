from portfolio.account_sync import AccountSync
from portfolio.holdings_sync import HoldingsSync
from portfolio.position_sync import PositionSync
from portfolio.sync import BrokerSyncService


# -------------------------
# Account Sync
# -------------------------


def test_account_sync_fetches_balance():

    class Broker:
        def get_funds(self):
            return {
                "cash": 100000
            }

    sync = AccountSync(
        broker=Broker()
    )

    assert sync.sync()["cash"] == 100000


def test_account_sync_without_broker():

    import pytest

    with pytest.raises(RuntimeError):
        AccountSync().sync()


def test_account_sync_reset():

    sync = AccountSync()

    sync.account_data["cash"] = 100

    sync.reset()

    assert sync.account_data == {}


def test_account_summary():

    sync = AccountSync()

    sync.account_data = {
        "cash": 100
    }

    assert sync.summary()["cash"] == 100


# -------------------------
# Holdings Sync
# -------------------------


def test_holdings_difference():

    sync = HoldingsSync()

    sync.set_local(
        "NIFTY",
        100,
    )

    sync.set_broker(
        "NIFTY",
        80,
    )

    assert sync.difference(
        "NIFTY"
    ) == 20


def test_holdings_in_sync():

    sync = HoldingsSync()

    sync.set_local(
        "NIFTY",
        100,
    )

    sync.set_broker(
        "NIFTY",
        100,
    )

    assert sync.is_in_sync()


def test_holdings_sync_from_broker():

    class Broker:

        def get_holdings(self):
            return [
                {
                    "securityId": "NIFTY",
                    "quantity": 10,
                }
            ]

    sync = HoldingsSync(
        broker=Broker()
    )

    sync.sync()

    assert sync.broker_holdings["NIFTY"] == 10


def test_holdings_reset():

    sync = HoldingsSync()

    sync.set_local(
        "NIFTY",
        10,
    )

    sync.reset()

    assert sync.local_holdings == {}


# -------------------------
# Position Sync
# -------------------------


def test_position_difference():

    sync = PositionSync()

    sync.set_local(
        "NIFTY",
        65,
    )

    sync.set_broker(
        "NIFTY",
        60,
    )

    assert sync.difference(
        "NIFTY"
    ) == 5


def test_position_sync_from_broker():

    class Broker:

        def get_positions(self):
            return [
                {
                    "securityId": "NIFTY",
                    "quantity": 65,
                }
            ]

    sync = PositionSync(
        broker=Broker()
    )

    sync.sync()

    assert sync.broker_positions["NIFTY"] == 65


def test_position_sync_without_broker():

    import pytest

    with pytest.raises(RuntimeError):
        PositionSync().sync()


# -------------------------
# Broker Sync Service
# -------------------------


def test_sync_all_success():

    class Sync:

        def sync(self):
            return "OK"


    service = BrokerSyncService(
        Sync(),
        Sync(),
        Sync(),
    )

    result = service.sync_all()

    assert result["errors"] == {}
    assert result["positions"] == "OK"


def test_sync_all_partial_failure():

    class Good:

        def sync(self):
            return "OK"


    class Bad:

        def sync(self):
            raise Exception(
                "failed"
            )


    service = BrokerSyncService(
        Bad(),
        Good(),
        Good(),
    )

    result = service.sync_all()

    assert "positions" in result["errors"]


def test_sync_all_keeps_other_results():

    class Good:

        def sync(self):
            return "OK"


    class Bad:

        def sync(self):
            raise Exception(
                "failed"
            )


    service = BrokerSyncService(
        Good(),
        Bad(),
        Good(),
    )

    result = service.sync_all()

    assert result["positions"] == "OK"
    assert result["account"] == "OK"


def test_holdings_remove_local():

    sync = HoldingsSync()

    sync.set_local(
        "ABC",
        10,
    )

    sync.remove_local(
        "ABC"
    )

    assert "ABC" not in sync.local_holdings


def test_position_remove_local():

    sync = PositionSync()

    sync.set_local(
        "ABC",
        10,
    )

    sync.remove_local(
        "ABC"
    )

    assert "ABC" not in sync.local_positions


def test_holdings_summary():

    sync = HoldingsSync()

    result = sync.summary()

    assert "in_sync" in result


def test_position_summary():

    sync = PositionSync()

    result = sync.summary()

    assert "in_sync" in result