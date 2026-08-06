"""
Terminal Operations Dashboard.
"""

from datetime import datetime

from dashboard.widgets.alert_widget import AlertWidget
from dashboard.widgets.broker_widget import BrokerWidget
from dashboard.widgets.market_widget import MarketWidget
from dashboard.widgets.portfolio_widget import PortfolioWidget
from dashboard.widgets.risk_widget import RiskWidget
from dashboard.widgets.runtime_widget import RuntimeWidget
from dashboard.widgets.system_widget import SystemWidget


class TerminalDashboard:
    """
    Terminal Operations Dashboard.
    """

    def __init__(
        self,
        runtime_widget=None,
        broker_widget=None,
        market_widget=None,
        portfolio_widget=None,
        risk_widget=None,
        system_widget=None,
        alert_widget=None,
    ) -> None:
        self.running = False
        self.started_at = None

        self.runtime_widget = runtime_widget or RuntimeWidget()
        self.broker_widget = broker_widget or BrokerWidget()
        self.market_widget = market_widget or MarketWidget()
        self.portfolio_widget = portfolio_widget or PortfolioWidget()
        self.risk_widget = risk_widget or RiskWidget()
        self.system_widget = system_widget or SystemWidget()
        self.alert_widget = alert_widget or AlertWidget()

    def start(self):
        self.running = True
        self.started_at = datetime.now()

    def stop(self):
        self.running = False

    def refresh(self):
        """
        Future hook for updating widgets.
        """

    def render(self):
        return (
            "\n"
            "============================================================\n"
            "        Trading Operating System Dashboard\n"
            "============================================================\n\n"
            + self.runtime_widget.render()
            + "\n"
            + self.broker_widget.render()
            + "\n"
            + self.market_widget.render()
            + "\n"
            + self.portfolio_widget.render()
            + "\n"
            + self.risk_widget.render()
            + "\n"
            + self.system_widget.render()
            + "\n"
            + self.alert_widget.render()
            + "\n============================================================\n"
        )