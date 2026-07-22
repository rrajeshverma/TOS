from persistence.position_repository import PositionRepository
from persistence.sqlite_repository import SQLiteRepository
from persistence.trade_repository import TradeRepository

# ---------------------------------------------------------------------
# TradeRepository
# ---------------------------------------------------------------------


def create_trade():
    return {
        "symbol": "NIFTY",
        "side": "BUY",
        "price": 250.50,
        "quantity": 50,
    }


def test_trade_repository_save():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    assert len(repo.get_all()) == 1


def test_trade_repository_get_by_id():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    trade = repo.get_by_id(1)

    assert trade["symbol"] == "NIFTY"


def test_trade_repository_find_by_symbol():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    trades = repo.find_by_symbol("NIFTY")

    assert len(trades) == 1


def test_trade_repository_update_status():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    repo.update_status(1, "CLOSED")

    assert repo.get_by_id(1)["status"] == "CLOSED"


def test_trade_repository_delete():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    repo.delete(1)

    assert repo.get_all() == []


def test_trade_repository_find_open():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    assert len(repo.find_open_trades()) == 1


def test_trade_repository_find_closed():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    repo.update_status(1, "CLOSED")

    assert len(repo.find_closed_trades()) == 1


def test_trade_repository_missing_trade():
    repo = TradeRepository(":memory:")

    assert repo.get_by_id(999) is None


# ---------------------------------------------------------------------
# PositionRepository
# ---------------------------------------------------------------------


def create_position():
    return {
        "symbol": "BANKNIFTY",
        "qty": 25,
    }


def test_position_repository_add():
    repo = PositionRepository()

    repo.add(create_position())

    assert repo.count() == 1


def test_position_repository_get():
    repo = PositionRepository()

    repo.add(create_position())

    assert repo.get("BANKNIFTY")["qty"] == 25


def test_position_repository_has_position():
    repo = PositionRepository()

    repo.add(create_position())

    assert repo.has_position("BANKNIFTY")


def test_position_repository_update():
    repo = PositionRepository()

    repo.add(create_position())

    repo.update(
        {
            "symbol": "BANKNIFTY",
            "qty": 100,
        }
    )

    assert repo.get("BANKNIFTY")["qty"] == 100


def test_position_repository_remove():
    repo = PositionRepository()

    repo.add(create_position())

    repo.remove("BANKNIFTY")

    assert repo.count() == 0


def test_position_repository_clear():
    repo = PositionRepository()

    repo.add(create_position())

    repo.clear()

    assert repo.get_all() == []


def test_position_repository_missing():
    repo = PositionRepository()

    assert repo.get("NONE") is None


def test_position_repository_multiple():
    repo = PositionRepository()

    repo.add(
        {
            "symbol": "NIFTY",
            "qty": 50,
        }
    )

    repo.add(
        {
            "symbol": "BANKNIFTY",
            "qty": 25,
        }
    )

    assert repo.count() == 2


# ---------------------------------------------------------------------
# SQLiteRepository
# ---------------------------------------------------------------------


def test_sqlite_repository_connection():
    repo = SQLiteRepository(":memory:")

    assert repo.connection is not None

    repo.close()


def test_sqlite_repository_close():
    repo = SQLiteRepository(":memory:")

    repo.close()

    assert True


def test_sqlite_repository_multiple_instances():
    repo1 = SQLiteRepository(":memory:")
    repo2 = SQLiteRepository(":memory:")

    assert repo1.connection is not repo2.connection

    repo1.close()
    repo2.close()


def test_trade_repository_multiple_trades():
    repo = TradeRepository(":memory:")

    repo.save(create_trade())

    repo.save(
        {
            "symbol": "BANKNIFTY",
            "side": "SELL",
            "price": 300,
            "quantity": 25,
        }
    )

    assert len(repo.get_all()) == 2
