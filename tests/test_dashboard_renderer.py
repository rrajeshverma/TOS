from dashboard.dashboard_model import DashboardModel
from dashboard.dashboard_renderer import DashboardRenderer
from dashboard.dashboard_service import DashboardService


def test_dashboard_renderer_returns_dict():
    renderer = DashboardRenderer()

    dashboard = DashboardModel()

    result = renderer.render(dashboard)

    assert isinstance(result, dict)


def test_dashboard_renderer_contains_sections():
    renderer = DashboardRenderer()
    dashboard = DashboardModel()

    result = renderer.render(dashboard)

    assert "portfolio_summary" in result
    assert "open_positions" in result
    assert "todays_pnl" in result
    assert "unrealized_pnl" in result
    assert "account_balance" in result
    assert "equity_curve" in result
    assert "performance" in result
    assert "risk" in result


def test_dashboard_renderer_renders_portfolio_summary_values():
    dashboard = DashboardModel()

    dashboard.portfolio_summary.total_value = 100000.0
    dashboard.portfolio_summary.cash = 25000.0

    renderer = DashboardRenderer()

    result = renderer.render(dashboard)

    assert result["portfolio_summary"]["total_value"] == 100000.0
    assert result["portfolio_summary"]["cash"] == 25000.0


def test_dashboard_renderer_renders_open_positions():
    dashboard = DashboardModel()

    dashboard.open_positions.positions.append(
        {
            "symbol": "NIFTY",
            "qty": 50,
            "pnl": 1250.0,
        }
    )
    dashboard.open_positions.count = 1

    renderer = DashboardRenderer()

    result = renderer.render(dashboard)

    assert result["open_positions"]["count"] == 1
    assert len(result["open_positions"]["positions"]) == 1
    assert result["open_positions"]["positions"][0]["symbol"] == "NIFTY"
    assert result["open_positions"]["positions"][0]["qty"] == 50
    assert result["open_positions"]["positions"][0]["pnl"] == 1250.0


def test_dashboard_renderer_renders_todays_pnl():
    dashboard = DashboardModel()

    dashboard.todays_pnl.realized_pnl = 4525.75
    dashboard.todays_pnl.trade_count = 4

    renderer = DashboardRenderer()

    result = renderer.render(dashboard)

    assert result["todays_pnl"]["realized_pnl"] == 4525.75
    assert result["todays_pnl"]["trade_count"] == 4


def test_dashboard_service_populates_portfolio_summary():
    service = DashboardService()

    dashboard = service.get_dashboard()

    assert dashboard.portfolio_summary.total_value >= 0.0
    assert dashboard.portfolio_summary.cash >= 0.0
    assert dashboard.portfolio_summary.invested >= 0.0
    assert dashboard.portfolio_summary.pnl >= 0.0
