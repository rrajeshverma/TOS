from backtesting.equity_curve import EquityCurve


def test_equity_curve():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 200},
    ]

    curve = EquityCurve(trades)

    assert curve.values() == [100, 50, 250]