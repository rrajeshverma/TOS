class CAGR:
    """Calculates Compound Annual Growth Rate."""

    def calculate(
        self,
        beginning_value: float,
        ending_value: float,
        years: float,
    ) -> float:
        if beginning_value <= 0:
            return 0.0

        if years <= 0:
            return 0.0

        return ((ending_value / beginning_value) ** (1 / years)) - 1
