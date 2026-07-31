from analytics.trade_statistics import TradeStatistics


def test_empty_statistics():
    stats = TradeStatistics([])

    assert stats.profit_factor == 0
    assert stats.expectancy == 0


def test_trade_statistics():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 200},
        {"pnl": -25},
    ]

    stats = TradeStatistics(trades)

    assert stats.profit_factor == 4.0
    assert stats.expectancy == 56.25
