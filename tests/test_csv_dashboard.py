from dashboard.csv_dashboard import CSVDashboard
from dashboard.dashboard_model import DashboardModel


def test_csv_dashboard_contains_portfolio_value():
    dashboard = DashboardModel()
    dashboard.portfolio_summary.total_value = 100000.0

    renderer = CSVDashboard()

    output = renderer.render(dashboard)

    assert "100000.0" in output
