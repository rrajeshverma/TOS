import pytest

from backtesting.trade_simulator import TradeSimulator


def test_trade_simulator_starts_empty():
    simulator = TradeSimulator()

    assert simulator.position is None
    assert simulator.trades == []


def test_open_position():
    simulator = TradeSimulator()

    signal = {
        "action": "BUY",
        "price": 100,
    }

    simulator.open(signal)

    assert simulator.position is not None
    assert simulator.position["action"] == "BUY"
    assert simulator.position["entry_price"] == 100


def test_close_position():
    simulator = TradeSimulator()

    simulator.open(
        {
            "action": "BUY",
            "price": 100,
        }
    )

    simulator.close(110)

    assert simulator.position is None
    assert len(simulator.trades) == 1

    trade = simulator.trades[0]

    assert trade["entry_price"] == 100
    assert trade["exit_price"] == 110
    assert trade["pnl"] == 10


def test_sell_trade_profit():
    simulator = TradeSimulator()

    simulator.open(
        {
            "action": "SELL",
            "price": 100,
        }
    )

    simulator.close(90)

    trade = simulator.trades[0]

    assert trade["pnl"] == 10


def test_sell_trade_loss():
    simulator = TradeSimulator()

    simulator.open(
        {
            "action": "SELL",
            "price": 100,
        }
    )

    simulator.close(110)

    trade = simulator.trades[0]

    assert trade["pnl"] == -10


def test_close_returns_trade():
    simulator = TradeSimulator()

    simulator.open(
        {
            "action": "BUY",
            "price": 100,
        }
    )

    trade = simulator.close(110)

    assert trade["entry_price"] == 100
    assert trade["exit_price"] == 110
    assert trade["pnl"] == 10


def test_open_when_position_already_exists():
    simulator = TradeSimulator()

    simulator.open(
        {
            "action": "BUY",
            "price": 100,
        }
    )

    with pytest.raises(
        RuntimeError,
        match="Position already open.",
    ):
        simulator.open(
            {
                "action": "BUY",
                "price": 105,
            }
        )


def test_close_without_open_position():
    simulator = TradeSimulator()

    with pytest.raises(
        RuntimeError,
        match="No open position.",
    ):
        simulator.close(100)


def test_unknown_action_raises_value_error():
    simulator = TradeSimulator()

    simulator.position = {
        "action": "HOLD",
        "entry_price": 100,
    }

    with pytest.raises(
        ValueError,
        match="Unknown action: HOLD",
    ):
        simulator.close(110)
