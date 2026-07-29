from __future__ import annotations

from domain.portfolio import Portfolio


class PortfolioService:
    """
    Application service responsible for maintaining the portfolio.
    """

    def __init__(
        self,
        update_engine,
        portfolio: Portfolio | None = None,
    ) -> None:
        self._update_engine = update_engine
        self._portfolio = portfolio or Portfolio()

    @property
    def portfolio(self) -> Portfolio:
        return self._portfolio

    def on_order_filled(
        self,
        *,
        symbol: str,
        side,
        quantity: int,
        price,
    ):
        return self._update_engine.apply_fill(
            portfolio=self._portfolio,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
        )

    def on_order_partially_filled(
        self,
        *,
        symbol: str,
        side,
        quantity: int,
        price,
    ):
        return self.on_order_filled(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
        )

    def on_order_cancelled(
        self,
        order_id=None,
        **_,
    ) -> None:
        # Nothing changes in the portfolio for a cancelled order.
        return None

    def positions(self):
        return self._portfolio.positions

    def get_position(
        self,
        symbol: str,
    ):
        for position in self._portfolio.positions:
            if position.symbol == symbol:
                return position

        return None

    def total_positions(self) -> int:
        return len(self._portfolio.positions)
