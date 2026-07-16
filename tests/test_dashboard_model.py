from dashboard.dashboard_model import DashboardModel
from dashboard.widgets.account_balance import AccountBalanceWidget
from dashboard.widgets.open_positions import OpenPositionsWidget
from dashboard.widgets.portfolio_summary import PortfolioSummary
from dashboard.widgets.todays_pnl import TodaysPnLWidget
from dashboard.widgets.unrealized_pnl import UnrealizedPnLWidget
from dashboard.widgets.equity_curve import EquityCurveWidget
from dashboard.widgets.performance_widget import PerformanceWidget
from dashboard.widgets.risk_widget import RiskWidget


def test_dashboard_model_defaults():
    dashboard = DashboardModel()

    assert isinstance(dashboard.portfolio_summary, PortfolioSummary)
    assert isinstance(dashboard.open_positions, OpenPositionsWidget)
    assert isinstance(dashboard.todays_pnl, TodaysPnLWidget)
    assert isinstance(dashboard.unrealized_pnl, UnrealizedPnLWidget)
    assert isinstance(dashboard.account_balance, AccountBalanceWidget)


def test_dashboard_model_contains_portfolio_summary():
    dashboard = DashboardModel()

    assert isinstance(dashboard.portfolio_summary, PortfolioSummary)

def test_dashboard_model_contains_analytics_widgets():
    dashboard = DashboardModel()

    assert isinstance(dashboard.equity_curve, EquityCurveWidget)
    assert isinstance(dashboard.performance, PerformanceWidget)
    assert isinstance(dashboard.risk, RiskWidget)