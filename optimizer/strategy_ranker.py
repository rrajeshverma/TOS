class StrategyRanker:
    def __init__(self, results):
        self._results = list(results)

    @property
    def results(self):
        return list(self._results)

    def sort(self, key):
        return sorted(
            self._results,
            key=key,
            reverse=True,
        )

    def best(self):
        if not self._results:
            return None

        return max(self._results, key=lambda r: r.score)

    def top(self, count):
        return self.sort(lambda r: r.score)[:count]

    def profitable(self):
        return [result for result in self._results if result.is_profitable]
