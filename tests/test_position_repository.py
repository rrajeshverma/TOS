from services.position_manager import PositionManager
from persistence.position_repository import PositionRepository


def test_add_and_get_position():
    repo = PositionRepository()

    position = {
        "symbol": "BTCUSDT",
        "quantity": 0.01,
        "avg_price": 65000.0,
        "side": "LONG",
    }

    repo.add(position)

    assert repo.get("BTCUSDT") == position


def test_get_all_positions():
    repo = PositionRepository()

    repo.add(
        {
            "symbol": "BTCUSDT",
            "quantity": 0.01,
            "avg_price": 65000.0,
            "side": "LONG",
        }
    )

    repo.add(
        {
            "symbol": "NIFTY",
            "quantity": 75,
            "avg_price": 25000.0,
            "side": "LONG",
        }
    )

    positions = repo.get_all()

    assert len(positions) == 2
    assert {p["symbol"] for p in positions} == {"BTCUSDT", "NIFTY"}


def test_remove_position():
    repo = PositionRepository()

    repo.add(
        {
            "symbol": "BTCUSDT",
            "quantity": 0.01,
            "avg_price": 65000.0,
            "side": "LONG",
        }
    )

    repo.remove("BTCUSDT")

    assert repo.get("BTCUSDT") is None


def test_has_position():
    repo = PositionRepository()

    repo.add(
        {
            "symbol": "BTCUSDT",
            "quantity": 0.01,
            "avg_price": 65000.0,
            "side": "LONG",
        }
    )

    assert repo.has_position("BTCUSDT") is True
    assert repo.has_position("NIFTY") is False


def test_position_count():
    repo = PositionRepository()

    assert repo.count() == 0

    repo.add(
        {
            "symbol": "BTCUSDT",
            "quantity": 0.01,
            "avg_price": 65000.0,
            "side": "LONG",
        }
    )

    repo.add(
        {
            "symbol": "NIFTY",
            "quantity": 50,
            "avg_price": 25200.0,
            "side": "LONG",
        }
    )

    assert repo.count() == 2


def test_clear_positions():
    repo = PositionRepository()

    repo.add(
        {
            "symbol": "BTCUSDT",
            "quantity": 0.01,
            "avg_price": 65000.0,
            "side": "LONG",
        }
    )

    repo.add(
        {
            "symbol": "NIFTY",
            "quantity": 50,
            "avg_price": 25200.0,
            "side": "LONG",
        }
    )

    repo.clear()

    assert repo.count() == 0
    assert repo.get_all() == []


def test_update_position():
    repo = PositionRepository()

    repo.add(
        {
            "symbol": "BTCUSDT",
            "quantity": 0.01,
            "avg_price": 65000.0,
            "side": "LONG",
        }
    )

    updated = {
        "symbol": "BTCUSDT",
        "quantity": 0.02,
        "avg_price": 64800.0,
        "side": "LONG",
    }

    repo.update(updated)

    position = repo.get("BTCUSDT")

    assert position["quantity"] == 0.02
    assert position["avg_price"] == 64800.0


from decimal import Decimal

from services.position_manager import PositionManager


def test_realized_pnl():
    manager = PositionManager()

    pnl = manager.realized_pnl(
        entry_price=Decimal("100"),
        exit_price=Decimal("110"),
        quantity=10,
    )

    assert pnl == Decimal("100")
