from backtesting.metrics import Metrics


def test_metrics_summary():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 200},
    ]

    metrics = Metrics(trades)

    assert metrics.total_trades == 3
    assert metrics.winning_trades == 2
    assert metrics.losing_trades == 1
    assert metrics.net_pnl == 250
