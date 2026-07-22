from backtesting.slippage import Slippage


def test_buy_slippage():
    trade = {
        "action": "BUY",
        "entry_price": 100,
        "exit_price": 120,
        "pnl": 20,
    }

    result = Slippage(2).apply(trade)

    assert result["entry_price"] == 102


def test_sell_slippage():
    trade = {
        "action": "SELL",
        "entry_price": 100,
        "exit_price": 80,
        "pnl": 20,
    }

    result = Slippage(2).apply(trade)

    assert result["entry_price"] == 98


import pytest


def test_unknown_action_raises_value_error():
    trade = {
        "action": "HOLD",
        "entry_price": 100,
        "exit_price": 100,
        "pnl": 0,
    }

    with pytest.raises(
        ValueError,
        match="Unknown action: HOLD",
    ):
        Slippage(2).apply(trade)
