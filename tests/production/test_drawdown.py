from reporting.reports.drawdown import Drawdown


def test_no_drawdown():
    d = Drawdown()

    equity = [100000, 101000, 102000]

    result = d.calculate(equity)

    assert result == 0.0


def test_simple_drawdown():
    d = Drawdown()

    equity = [100000, 95000]

    result = d.calculate(equity)

    assert result == 5000.0


def test_multiple_drawdown():
    d = Drawdown()

    equity = [
        100000,
        110000,
        105000,
        98000,
        120000,
        118000,
    ]

    result = d.calculate(equity)

    assert result == 12000.0


def test_empty_equity():
    d = Drawdown()

    assert d.calculate([]) == 0.0


def test_single_equity():
    d = Drawdown()

    assert d.calculate([100000]) == 0.0
