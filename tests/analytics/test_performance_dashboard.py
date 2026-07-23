from analytics.performance_dashboard import PerformanceDashboard


def test_empty_dashboard():
    dashboard = PerformanceDashboard(
        initial_capital=100000,
        trades=[],
    )

    assert dashboard.metrics["initial_capital"] == 100000
    assert dashboard.metrics["final_capital"] == 100000
    assert dashboard.metrics["net_profit"] == 0
    assert dashboard.metrics["win_rate"] == 0


def test_dashboard_metrics():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 200},
        {"pnl": -25},
    ]

    dashboard = PerformanceDashboard(
        initial_capital=100000,
        trades=trades,
    )

    assert dashboard.metrics["initial_capital"] == 100000
    assert dashboard.metrics["final_capital"] == 100225
    assert dashboard.metrics["net_profit"] == 225
    assert dashboard.metrics["profit_factor"] == 4.0
    assert dashboard.metrics["win_rate"] == 50.0
