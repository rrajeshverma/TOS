from statistics import mean, median


class Statistics:
    def __init__(self):
        self._values = []

    def add(self, value):
        self._values.append(float(value))

    def clear(self):
        self._values.clear()

    @property
    def count(self):
        return len(self._values)

    @property
    def minimum(self):
        return min(self._values) if self._values else 0.0

    @property
    def maximum(self):
        return max(self._values) if self._values else 0.0

    @property
    def average(self):
        return mean(self._values) if self._values else 0.0

    @property
    def median(self):
        return median(self._values) if self._values else 0.0

    @property
    def total(self):
        return sum(self._values)

    def values(self):
        return list(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return (
            f"Statistics(count={self.count}, "
            f"avg={self.average:.2f})"
        )