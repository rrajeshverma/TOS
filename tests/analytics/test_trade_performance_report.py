from analytics.trade_performance_report import TradePerformanceReport


def test_empty_report():
    report = TradePerformanceReport([])
    assert report.total_trades == 0
    assert report.winning_trades == 0
    assert report.losing_trades == 0
    assert report.net_profit == 0


def test_report_statistics():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 200},
        {"pnl": -25},
    ]

    report = TradePerformanceReport(trades)

    assert report.total_trades == 4
    assert report.winning_trades == 2
    assert report.losing_trades == 2
    assert report.gross_profit == 300
    assert report.gross_loss == 75
    assert report.net_profit == 225
    assert report.win_rate == 50.0
