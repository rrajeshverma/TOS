from persistence.trade_repository import TradeRepository


def test_save_trade():
    repo = TradeRepository(":memory:")

    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 65000.0,
        "quantity": 0.01,
    }

    repo.save(trade)

    trades = repo.get_all()

    assert len(trades) == 1
    assert trades[0]["symbol"] == "BTCUSDT"
    assert trades[0]["side"] == "BUY"
    assert trades[0]["price"] == 65000.0
    assert trades[0]["quantity"] == 0.01


def test_get_trade_by_id():
    repo = TradeRepository(":memory:")

    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 65000.0,
        "quantity": 0.01,
    }

    repo.save(trade)

    saved_trade = repo.get_all()[0]

    result = repo.get_by_id(saved_trade["id"])

    assert result["id"] == saved_trade["id"]
    assert result["symbol"] == "BTCUSDT"
    assert result["side"] == "BUY"


def test_find_trades_by_symbol():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
        }
    )

    repo.save(
        {
            "symbol": "ETHUSDT",
            "side": "BUY",
            "price": 3500.0,
            "quantity": 0.10,
        }
    )

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "price": 65500.0,
            "quantity": 0.01,
        }
    )

    trades = repo.find_by_symbol("BTCUSDT")

    assert len(trades) == 2
    assert all(trade["symbol"] == "BTCUSDT" for trade in trades)


def test_update_trade_status():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
            "status": "OPEN",
        }
    )

    trade = repo.get_all()[0]

    repo.update_status(trade["id"], "CLOSED")

    updated = repo.get_by_id(trade["id"])

    assert updated["status"] == "CLOSED"


def test_delete_trade():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
        }
    )

    trade = repo.get_all()[0]

    repo.delete(trade["id"])

    assert repo.get_by_id(trade["id"]) is None


def test_find_open_trades():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
            "status": "OPEN",
        }
    )

    repo.save(
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "price": 3500.0,
            "quantity": 0.10,
            "status": "CLOSED",
        }
    )

    repo.save(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "price": 25000.0,
            "quantity": 75,
            "status": "OPEN",
        }
    )

    trades = repo.find_open_trades()

    assert len(trades) == 2
    assert all(trade["status"] == "OPEN" for trade in trades)


def test_find_closed_trades():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
            "status": "OPEN",
        }
    )

    repo.save(
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "price": 3500.0,
            "quantity": 0.10,
            "status": "CLOSED",
        }
    )

    repo.save(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "price": 25000.0,
            "quantity": 75,
            "status": "CLOSED",
        }
    )

    trades = repo.find_closed_trades()

    assert len(trades) == 2
    assert all(trade["status"] == "CLOSED" for trade in trades)


def test_find_open_trades_returns_only_open():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
            "status": "OPEN",
        }
    )

    repo.save(
        {
            "symbol": "ETHUSDT",
            "side": "BUY",
            "price": 3500.0,
            "quantity": 0.10,
            "status": "CLOSED",
        }
    )

    trades = repo.find_open_trades()

    assert len(trades) == 1
    assert trades[0]["symbol"] == "BTCUSDT"
    assert trades[0]["status"] == "OPEN"


def test_find_closed_trades_returns_only_closed():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
            "status": "OPEN",
        }
    )

    repo.save(
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "price": 3500.0,
            "quantity": 0.10,
            "status": "CLOSED",
        }
    )

    trades = repo.find_closed_trades()

    assert len(trades) == 1
    assert trades[0]["symbol"] == "ETHUSDT"
    assert trades[0]["status"] == "CLOSED"


def test_find_by_symbol_returns_empty_when_not_found():
    repo = TradeRepository(":memory:")

    repo.save(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": 65000.0,
            "quantity": 0.01,
        }
    )

    trades = repo.find_by_symbol("SOLUSDT")

    assert trades == []


def test_get_by_id_returns_none_when_not_found():
    repo = TradeRepository(":memory:")

    result = repo.get_by_id(99999)

    assert result is None


def test_delete_nonexistent_trade():
    repo = TradeRepository(":memory:")

    repo.delete(99999)

    assert repo.get_all() == []
