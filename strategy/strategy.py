class Strategy:
    """Base strategy contract."""

    def decide(self, indicators):
        if indicators is None:
            raise ValueError("indicators cannot be None")

        return "HOLD"
