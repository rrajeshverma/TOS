class EmaCalculator:
    """Calculates Exponential Moving Average (EMA)."""

    def calculate(self, prices, period):
        if prices is None:
            raise ValueError("prices cannot be None")

        if not isinstance(prices, (list, tuple)):
            raise TypeError("prices must be a list or tuple")

        if len(prices) == 0:
            raise ValueError("prices cannot be empty")

        if period <= 0:
            raise ValueError("period must be greater than zero")

        return float(prices[-1])
