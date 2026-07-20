from dataclasses import dataclass, field

from dashboard.widgets.account_balance import AccountBalanceWidget
from dashboard.widgets.equity_curve import EquityCurveWidget
from dashboard.widgets.open_positions import OpenPositionsWidget
from dashboard.widgets.performance_widget import PerformanceWidget
from dashboard.widgets.portfolio_summary import PortfolioSummary
from dashboard.widgets.risk_widget import RiskWidget
from dashboard.widgets.todays_pnl import TodaysPnLWidget
from dashboard.widgets.unrealized_pnl import UnrealizedPnLWidget


@dataclass
class DashboardModel:
    portfolio_summary: PortfolioSummary = field(default_factory=PortfolioSummary)
    open_positions: OpenPositionsWidget = field(default_factory=OpenPositionsWidget)
    todays_pnl: TodaysPnLWidget = field(default_factory=TodaysPnLWidget)
    unrealized_pnl: UnrealizedPnLWidget = field(default_factory=UnrealizedPnLWidget)
    account_balance: AccountBalanceWidget = field(default_factory=AccountBalanceWidget)
    equity_curve: EquityCurveWidget = field(default_factory=EquityCurveWidget)
    performance: PerformanceWidget = field(default_factory=PerformanceWidget)
    risk: RiskWidget = field(default_factory=RiskWidget)
