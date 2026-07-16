from domain.portfolio import Portfolio
from storage.portfolio_repository import PortfolioRepository


class HoldingsService:
    """Service for managing portfolio holdings and positions."""

    def __init__(self, repository: PortfolioRepository):
        self._repository = repository

    def get_holdings_count(self) -> int:
        portfolio = self._repository.get()
        return portfolio.holdings if portfolio else 0

    def get_positions_count(self) -> int:
        portfolio = self._repository.get()
        return portfolio.positions if portfolio else 0

    def get_realized_pnl(self) -> float:
        portfolio = self._repository.get()
        return portfolio.realized_pnl if portfolio else 0.0

    def get_unrealized_pnl(self) -> float:
        portfolio = self._repository.get()
        return portfolio.unrealized_pnl if portfolio else 0.0

    def update(self, portfolio: Portfolio) -> None:
        self._repository.save(portfolio)