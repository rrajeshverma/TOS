from dashboard.dashboard_model import DashboardModel
from dashboard.dashboard_service import DashboardService


def test_dashboard_service_returns_dashboard_model():
    service = DashboardService()

    dashboard = service.get_dashboard()

    assert isinstance(dashboard, DashboardModel)

def test_dashboard_service_returns_dashboard_with_widgets():
    service = DashboardService()

    dashboard = service.get_dashboard()

    assert dashboard.portfolio_summary is not None
    assert dashboard.open_positions is not None
    assert dashboard.todays_pnl is not None
    assert dashboard.unrealized_pnl is not None
    assert dashboard.account_balance is not None
    assert dashboard.equity_curve is not None
    assert dashboard.performance is not None
    assert dashboard.risk is not None

class FakePortfolioService:
    def get_summary(self):
        return {
            "total_value": 100000.0,
            "cash": 25000.0,
            "invested": 75000.0,
            "pnl": 5000.0,
        }


def test_dashboard_service_populates_portfolio_summary():
    service = DashboardService(
        portfolio_service=FakePortfolioService()
    )

    dashboard = service.get_dashboard()

    assert dashboard.portfolio_summary.total_value == 100000.0
    assert dashboard.portfolio_summary.cash == 25000.0
    assert dashboard.portfolio_summary.invested == 75000.0
    assert dashboard.portfolio_summary.pnl == 5000.0

class FakeTradeJournalService:
    def get_today_summary(self):
        return {
            "realized_pnl": 4525.75,
            "trade_count": 4,
        }


def test_dashboard_service_populates_todays_pnl():
    service = DashboardService(
        trade_journal_service=FakeTradeJournalService()
    )

    dashboard = service.get_dashboard()

    assert dashboard.todays_pnl.realized_pnl == 4525.75
    assert dashboard.todays_pnl.trade_count == 4

class FakeFundsService:
    def get_account_balance(self):
        return {
            "balance": 500000.0,
            "available_margin": 425000.0,
        }


def test_dashboard_service_populates_account_balance():
    service = DashboardService(
        funds_service=FakeFundsService()
    )

    dashboard = service.get_dashboard()

    assert dashboard.account_balance.balance == 500000.0
    assert dashboard.account_balance.available_margin == 425000.0

class FakePositionService:
    def get_open_positions(self):
        return [
            {
                "symbol": "NIFTY",
                "qty": 50,
                "pnl": 1250.0,
            },
            {
                "symbol": "BANKNIFTY",
                "qty": 25,
                "pnl": -350.0,
            },
        ]


def test_dashboard_service_populates_open_positions():
    service = DashboardService(
        position_service=FakePositionService()
    )

    dashboard = service.get_dashboard()

    assert dashboard.open_positions.count == 2
    assert len(dashboard.open_positions.positions) == 2
    assert dashboard.open_positions.positions[0]["symbol"] == "NIFTY"
    assert dashboard.open_positions.positions[1]["symbol"] == "BANKNIFTY"

class FakePerformanceService:
    def get_performance(self):
        return {
            "win_rate": 62.5,
            "total_trades": 40,
            "average_profit": 1850.0,
            "average_loss": 950.0,
        }


def test_dashboard_service_populates_performance():
    service = DashboardService(
        performance_service=FakePerformanceService()
    )

    dashboard = service.get_dashboard()

    assert dashboard.performance.win_rate == 62.5
    assert dashboard.performance.total_trades == 40
    assert dashboard.performance.average_profit == 1850.0
    assert dashboard.performance.average_loss == 950.0

class FakeRiskService:
    def get_risk_metrics(self):
        return {
            "max_drawdown": 8.5,
            "current_risk": 2.0,
            "risk_reward_ratio": 2.5,
        }


def test_dashboard_service_populates_risk():
    service = DashboardService(
        risk_service=FakeRiskService()
    )

    dashboard = service.get_dashboard()

    assert dashboard.risk.max_drawdown == 8.5
    assert dashboard.risk.current_risk == 2.0
    assert dashboard.risk.risk_reward_ratio == 2.5

def test_dashboard_service_populates_complete_dashboard():
    service = DashboardService(
        portfolio_service=FakePortfolioService(),
        position_service=FakePositionService(),
        trade_journal_service=FakeTradeJournalService(),
        funds_service=FakeFundsService(),
        performance_service=FakePerformanceService(),
        risk_service=FakeRiskService(),
    )

    dashboard = service.get_dashboard()

    assert dashboard.portfolio_summary.total_value == 100000.0
    assert dashboard.open_positions.count == 2
    assert dashboard.todays_pnl.trade_count == 4
    assert dashboard.account_balance.balance == 500000.0
    assert dashboard.performance.total_trades == 40
    assert dashboard.risk.risk_reward_ratio == 2.5