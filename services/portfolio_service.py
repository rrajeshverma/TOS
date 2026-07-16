from domain.portfolio import Portfolio
from storage.portfolio_repository import PortfolioRepository


class PortfolioService:
    """Service for managing the trading portfolio."""

    def __init__(self, repository: PortfolioRepository):
        self._repository = repository

    def get_portfolio(self) -> Portfolio | None:
        return self._repository.get()

    def get_account_id(self) -> str | None:
        portfolio = self._repository.get()
        return portfolio.account_id if portfolio else None

    def update(self, portfolio: Portfolio) -> None:
        self._repository.save(portfolio)

    def clear(self) -> None:
        self._repository.clear()

    def exists(self) -> bool:
        return self._repository.exists()