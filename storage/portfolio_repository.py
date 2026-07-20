from domain.portfolio import Portfolio


class PortfolioRepository:
    """In-memory repository for Portfolio."""

    def __init__(self):
        self._portfolio: Portfolio | None = None

    def save(self, portfolio: Portfolio) -> None:
        self._portfolio = portfolio

    def get(self) -> Portfolio | None:
        return self._portfolio

    def clear(self) -> None:
        self._portfolio = None

    def exists(self) -> bool:
        return self._portfolio is not None
