from reporting.reports.equity_curve import EquityCurve


def test_empty_curve():
    curve = EquityCurve()

    assert curve.build([]) == []


def test_single_trade():
    curve = EquityCurve()

    assert curve.build([100]) == [100]


def test_running_equity():
    curve = EquityCurve()

    pnl = [100, -50, 200]

    assert curve.build(pnl) == [100, 50, 250]


def test_all_losses():
    curve = EquityCurve()

    pnl = [-100, -50, -25]

    assert curve.build(pnl) == [-100, -150, -175]


def test_zero_values():
    curve = EquityCurve()

    pnl = [0, 0, 0]

    assert curve.build(pnl) == [0, 0, 0]


def test_large_series():
    curve = EquityCurve()

    pnl = [10] * 100

    result = curve.build(pnl)

    assert result[-1] == 1000
    assert len(result) == 100