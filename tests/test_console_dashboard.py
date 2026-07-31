from dashboard.console_dashboard import ConsoleDashboard
from dashboard.dashboard_model import DashboardModel


def test_console_dashboard_render_returns_string():
    dashboard = DashboardModel()
    console = ConsoleDashboard()

    output = console.render(dashboard)

    assert isinstance(output, str)


def test_console_dashboard_contains_portfolio_value():
    dashboard = DashboardModel()
    dashboard.portfolio_summary.total_value = 100000.0

    console = ConsoleDashboard()

    output = console.render(dashboard)

    assert "100000.0" in output
