from analytics.trade_analyzer import TradeAnalyzer


def test_largest_win():
    analyzer = TradeAnalyzer()

    assert analyzer.largest_win([100, -50, 250, -100]) == 250


def test_largest_loss():
    analyzer = TradeAnalyzer()

    assert analyzer.largest_loss([100, -50, 250, -100]) == -100


def test_consecutive_wins():
    analyzer = TradeAnalyzer()

    trades = [100, 200, -50, 300, 400, 500]

    assert analyzer.max_consecutive_wins(trades) == 3


def test_consecutive_losses():
    analyzer = TradeAnalyzer()

    trades = [100, -50, -25, -10, 200, -5]

    assert analyzer.max_consecutive_losses(trades) == 3