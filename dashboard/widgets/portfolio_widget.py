"""
Portfolio Dashboard Widget.
"""


class PortfolioWidget:
    """
    Displays portfolio information.
    """

    def __init__(
        self,
        cash=0.0,
        exposure=0.0,
        pnl=0.0,
        positions=0,
    ) -> None:
        self.cash = cash
        self.exposure = exposure
        self.pnl = pnl
        self.positions = positions

    def render(self) -> str:
        """
        Render portfolio information.
        """

        return (
            "Portfolio\n"
            f"Cash      : ₹{self.cash:,.2f}\n"
            f"Exposure  : ₹{self.exposure:,.2f}\n"
            f"PnL       : ₹{self.pnl:,.2f}\n"
            f"Positions : {self.positions}\n"
        )
