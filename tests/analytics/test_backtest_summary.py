from analytics.backtest_summary import BacktestSummary


def test_empty_summary():
    summary = BacktestSummary(
        initial_capital=100000,
        trades=[],
    )

    assert summary.initial_capital == 100000
    assert summary.final_capital == 100000
    assert summary.total_trades == 0
    assert summary.net_profit == 0
    assert summary.win_rate == 0


def test_backtest_summary():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 200},
        {"pnl": -25},
    ]

    summary = BacktestSummary(
        initial_capital=100000,
        trades=trades,
    )

    assert summary.initial_capital == 100000
    assert summary.final_capital == 100225
    assert summary.total_trades == 4
    assert summary.net_profit == 225
    assert summary.win_rate == 50.0
    assert summary.profit_factor == 4.0
