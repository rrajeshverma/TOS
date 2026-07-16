from domain.portfolio import Portfolio
from storage.portfolio_repository import PortfolioRepository


class FundsService:
    """Service for managing account funds."""

    def __init__(self, repository: PortfolioRepository):
        self._repository = repository

    def get_cash(self) -> float:
        portfolio = self._repository.get()
        return portfolio.cash if portfolio else 0.0

    def get_available_margin(self) -> float:
        portfolio = self._repository.get()
        return portfolio.available_margin if portfolio else 0.0

    def get_used_margin(self) -> float:
        portfolio = self._repository.get()
        return portfolio.used_margin if portfolio else 0.0

    def get_equity(self) -> float:
        portfolio = self._repository.get()
        return portfolio.equity if portfolio else 0.0

    def update(self, portfolio: Portfolio) -> None:
        self._repository.save(portfolio)