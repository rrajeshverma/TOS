"""
TOS NIFTY Opening Range Breakout Strategy

First production strategy plugin.
"""

from __future__ import annotations

from strategies.base_strategy import BaseStrategy


class NiftyORBStrategy(BaseStrategy):
    """
    NIFTY Opening Range Breakout strategy.
    """


    def name(self) -> str:
        return "NIFTY_ORB"


    def analyze(
        self,
        context,
    ):
        """
        Analyze market context.
        """

        return {
            "strategy": self.name(),
            "analyzed": True,
            "context_available": context is not None,
        }


    def generate_signal(
        self,
        context,
    ):
        """
        Generate trading signal.

        Rules:
        - Price above opening high  -> BUY
        - Price below opening low   -> SELL
        - Otherwise                 -> WAIT
        """

        if context is None:
            return None


        current_price = context.get(
            "current_price"
        )


        if (
            "opening_high" in context
            and current_price > context["opening_high"]
        ):
            return "BUY"


        if (
            "opening_low" in context
            and current_price < context["opening_low"]
        ):
            return "SELL"


        return "WAIT"
