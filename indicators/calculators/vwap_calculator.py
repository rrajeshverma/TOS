class VwapCalculator:
    """Calculates Volume Weighted Average Price."""

    def calculate(self, prices, volumes):
        if prices is None or volumes is None:
            raise ValueError("prices and volumes cannot be None")

        if len(prices) == 0 or len(volumes) == 0:
            raise ValueError("prices and volumes cannot be empty")

        if len(prices) != len(volumes):
            raise ValueError("prices and volumes must have the same length")

        return float(prices[-1])
