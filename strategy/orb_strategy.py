class OrbStrategy:
    """Opening Range Breakout strategy."""

    def decide(self, indicators):
        if indicators is None:
            raise ValueError("indicators cannot be None")

        if indicators.rsi < 30:
            return "BUY"

        if indicators.rsi > 70:
            return "SELL"

        return "HOLD"
