from analytics.equity_curve import EquityCurve


def test_empty_equity_curve():
    curve = EquityCurve(100000, [])
    assert curve.points == [100000]


def test_equity_curve():
    trades = [500, -200, 300]

    curve = EquityCurve(100000, trades)

    assert curve.points == [
        100000,
        100500,
        100300,
        100600,
    ]
