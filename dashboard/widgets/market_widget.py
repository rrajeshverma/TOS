"""
Market Dashboard Widget.
"""


class MarketWidget:
    """
    Displays market information.
    """

    def __init__(
        self,
        session="CLOSED",
        symbol="NIFTY",
        price=0.0,
        last_tick="--:--:--",
    ) -> None:
        self.session = session
        self.symbol = symbol
        self.price = price
        self.last_tick = last_tick

    def render(self) -> str:
        """
        Render market information.
        """

        return (
            "Market\n"
            f"Session  : {self.session}\n"
            f"Symbol   : {self.symbol}\n"
            f"Price    : {self.price}\n"
            f"LastTick : {self.last_tick}\n"
        )
