from dashboard.dashboard_model import DashboardModel


class DashboardService:
    def __init__(
        self,
        portfolio_service=None,
        trade_journal_service=None,
        funds_service=None,
        position_service=None,
        performance_service=None,
        risk_service=None,
    ):
        self.portfolio_service = portfolio_service
        self.trade_journal_service = trade_journal_service
        self.funds_service = funds_service
        self.position_service = position_service
        self.performance_service = performance_service
        self.risk_service = risk_service

    def get_dashboard(self) -> DashboardModel:
        dashboard = DashboardModel()

        if self.portfolio_service:
            summary = self.portfolio_service.get_summary()

            dashboard.portfolio_summary.total_value = summary["total_value"]
            dashboard.portfolio_summary.cash = summary["cash"]
            dashboard.portfolio_summary.invested = summary["invested"]
            dashboard.portfolio_summary.pnl = summary["pnl"]

        if self.position_service:
            positions = self.position_service.get_open_positions()

            dashboard.open_positions.positions = positions
            dashboard.open_positions.count = len(positions)

        if self.performance_service:
            performance = self.performance_service.get_performance()

            dashboard.performance.win_rate = performance["win_rate"]
            dashboard.performance.total_trades = performance["total_trades"]
            dashboard.performance.average_profit = performance["average_profit"]
            dashboard.performance.average_loss = performance["average_loss"]

        if self.risk_service:
            risk = self.risk_service.get_risk_metrics()

            dashboard.risk.max_drawdown = risk["max_drawdown"]
            dashboard.risk.current_risk = risk["current_risk"]
            dashboard.risk.risk_reward_ratio = risk["risk_reward_ratio"]

        if self.trade_journal_service:
            today = self.trade_journal_service.get_today_summary()

            dashboard.todays_pnl.realized_pnl = today["realized_pnl"]
            dashboard.todays_pnl.trade_count = today["trade_count"]

        if self.funds_service:
            account = self.funds_service.get_account_balance()

            dashboard.account_balance.balance = account["balance"]
            dashboard.account_balance.available_margin = account["available_margin"]

        return dashboard