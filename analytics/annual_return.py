class AnnualReturn:
    """Calculates simple annual return."""

    def calculate(
        self,
        beginning_value: float,
        ending_value: float,
    ) -> float:

        if beginning_value <= 0:
            return 0.0

        return (ending_value - beginning_value) / beginning_value
