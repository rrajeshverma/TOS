from analytics.equity_analytics import EquityAnalytics

# ============================================================
# Construction
# ============================================================


def test_initial_equity():
    analytics = EquityAnalytics(10000)

    assert analytics.initial_equity == 10000


def test_initial_curve():
    analytics = EquityAnalytics(10000)

    assert analytics.equity_curve() == [10000]


# ============================================================
# Add Trades
# ============================================================


def test_single_trade():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)

    assert analytics.equity_curve() == [10000, 10500]


def test_multiple_trades():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)
    analytics.add_trade(-200)

    assert analytics.equity_curve() == [10000, 10500, 10300]


# ============================================================
# Current Equity
# ============================================================


def test_current_equity():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)

    assert analytics.current_equity() == 10500


def test_current_equity_loss():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(-500)

    assert analytics.current_equity() == 9500


# ============================================================
# Peak Equity
# ============================================================


def test_peak_equity():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)
    analytics.add_trade(-100)

    assert analytics.peak_equity() == 10500


# ============================================================
# Maximum Drawdown
# ============================================================


def test_max_drawdown():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)
    analytics.add_trade(-1000)

    assert analytics.max_drawdown() == 1000


def test_zero_drawdown():
    analytics = EquityAnalytics(10000)

    assert analytics.max_drawdown() == 0


# ============================================================
# Summary
# ============================================================


def test_summary_current_equity():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(100)

    assert analytics.summary()["current_equity"] == 10100


def test_summary_peak_equity():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(100)

    assert analytics.summary()["peak_equity"] == 10100


def test_summary_drawdown():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)
    analytics.add_trade(-1000)

    assert analytics.summary()["max_drawdown"] == 1000


def test_summary_initial_equity():
    analytics = EquityAnalytics(10000)

    assert analytics.summary()["initial_equity"] == 10000


# ============================================================
# Curve Size
# ============================================================


def test_curve_length():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(100)
    analytics.add_trade(200)

    assert len(analytics.equity_curve()) == 3


def test_curve_last_value():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(100)
    analytics.add_trade(200)

    assert analytics.equity_curve()[-1] == 10300


# ============================================================
# Total Return
# ============================================================


def test_total_return():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(500)

    assert analytics.total_return() == 500


def test_total_return_loss():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(-500)

    assert analytics.total_return() == -500


# ============================================================
# Return Percent
# ============================================================


def test_return_percent():
    analytics = EquityAnalytics(10000)

    analytics.add_trade(1000)

    assert analytics.return_percent() == 10.0


def test_return_percent_zero():
    analytics = EquityAnalytics(10000)

    assert analytics.return_percent() == 0.0


def test_return_percent_zero_initial_equity():
    analytics = EquityAnalytics(0)

    assert analytics.return_percent() == 0.0
