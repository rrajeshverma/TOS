from collections import deque


class LatencyTracker:
    def __init__(self, max_samples=1000):
        self._samples = deque(maxlen=max_samples)

    def add(self, latency):
        self._samples.append(float(latency))

    @property
    def count(self):
        return len(self._samples)

    @property
    def minimum(self):
        if not self._samples:
            return 0.0
        return min(self._samples)

    @property
    def maximum(self):
        if not self._samples:
            return 0.0
        return max(self._samples)

    @property
    def average(self):
        if not self._samples:
            return 0.0
        return sum(self._samples) / len(self._samples)

    def clear(self):
        self._samples.clear()

    def values(self):
        return list(self._samples)

    def latest(self):
        if not self._samples:
            return 0.0
        return self._samples[-1]

    def __len__(self):
        return len(self._samples)

    def __repr__(self):
        return f"LatencyTracker(count={self.count}, avg={self.average:.6f})"
