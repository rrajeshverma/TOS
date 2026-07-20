from dataclasses import asdict

from dashboard.dashboard_model import DashboardModel


class DashboardRenderer:
    def render(self, dashboard: DashboardModel) -> dict:
        return {
            "portfolio_summary": asdict(dashboard.portfolio_summary),
            "open_positions": asdict(dashboard.open_positions),
            "todays_pnl": asdict(dashboard.todays_pnl),
            "unrealized_pnl": asdict(dashboard.unrealized_pnl),
            "account_balance": asdict(dashboard.account_balance),
            "equity_curve": asdict(dashboard.equity_curve),
            "performance": asdict(dashboard.performance),
            "risk": asdict(dashboard.risk),
        }
