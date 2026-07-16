from domain.portfolio import Portfolio
from services.portfolio_service import PortfolioService


class AccountSynchronizer:
    """Synchronizes broker account data with the local portfolio."""

    def __init__(self, broker, portfolio_service: PortfolioService):
        self._broker = broker
        self._portfolio_service = portfolio_service
        self._last_portfolio: Portfolio | None = None

    def sync(self) -> Portfolio:
        """
        Fetch the latest portfolio from the broker and
        update the local portfolio service.
        """
        portfolio = self._broker.get_portfolio()

        self._portfolio_service.update(portfolio)

        self._last_portfolio = portfolio

        return portfolio

    def last_portfolio(self) -> Portfolio | None:
        """Return the last synchronized portfolio."""
        return self._last_portfolio