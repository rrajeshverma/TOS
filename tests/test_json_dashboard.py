from dashboard.dashboard_model import DashboardModel
from dashboard.json_dashboard import JSONDashboard


def test_json_dashboard_contains_portfolio_value():
    dashboard = DashboardModel()
    dashboard.portfolio_summary.total_value = 100000.0

    renderer = JSONDashboard()

    output = renderer.render(dashboard)

    assert "100000.0" in output