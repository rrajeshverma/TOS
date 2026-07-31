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


def test_analyze_empty():
    analyzer = TradeAnalyzer()

    result = analyzer.analyze([])

    assert result["trade_count"] == 0
    assert result["winning_trades"] == 0
    assert result["losing_trades"] == 0
    assert result["largest_win"] == 0
    assert result["largest_loss"] == 0
    assert result["max_consecutive_wins"] == 0
    assert result["max_consecutive_losses"] == 0


def test_analyze_summary():
    analyzer = TradeAnalyzer()

    trades = [100, 200, -50, -25, 300]

    result = analyzer.analyze(trades)

    assert result["largest_win"] == 300
    assert result["largest_loss"] == -50
    assert result["max_consecutive_wins"] == 2
    assert result["max_consecutive_losses"] == 2


def test_analyze_trade_count():
    analyzer = TradeAnalyzer()

    result = analyzer.analyze([100, -50, 200])

    assert result["trade_count"] == 3


def test_analyze_win_loss_count():
    analyzer = TradeAnalyzer()

    result = analyzer.analyze([100, -50, 200, -20])

    assert result["winning_trades"] == 2
    assert result["losing_trades"] == 2
