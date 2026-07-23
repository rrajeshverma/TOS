from analytics.drawdown_analyzer import DrawdownAnalyzer


def test_empty_drawdown():
    analyzer = DrawdownAnalyzer([100000])

    assert analyzer.max_drawdown == 0
    assert analyzer.current_drawdown == 0


def test_drawdown():
    equity = [
        100000,
        101000,
        99500,
        102000,
        100000,
    ]

    analyzer = DrawdownAnalyzer(equity)

    assert analyzer.max_drawdown == 2000
    assert analyzer.current_drawdown == 2000
