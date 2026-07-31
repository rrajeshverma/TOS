class VolumeAverageCalculator:
    """Calculates average traded volume."""

    def calculate(self, volumes):
        if volumes is None:
            raise ValueError("volumes cannot be None")

        if len(volumes) == 0:
            raise ValueError("volumes cannot be empty")

        return float(sum(volumes) / len(volumes))
