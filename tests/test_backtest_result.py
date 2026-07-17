from backtesting.backtest_result import BacktestResult


def test_empty_result():
    result = BacktestResult()

    assert result.trades == []
    assert result.total_trades == 0
    assert result.net_pnl == 0


def test_add_trade():
    result = BacktestResult()

    result.add_trade({
        "pnl": 100
    })

    assert result.total_trades == 1
    assert result.net_pnl == 100


def test_multiple_trades():
    result = BacktestResult()

    result.add_trade({"pnl": 100})
    result.add_trade({"pnl": -30})
    result.add_trade({"pnl": 50})

    assert result.total_trades == 3
    assert result.net_pnl == 120


def test_returns_trade_list():
    result = BacktestResult()

    trade = {"pnl": 25}

    result.add_trade(trade)

    assert result.trades[0] == trade


def test_zero_trade_result():
    result = BacktestResult()

    assert result.net_pnl == 0