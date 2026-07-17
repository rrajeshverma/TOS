from optimizer.optimization_result import OptimizationResult


class BaseSearch:
    def __init__(self):
        self._results = []

    @property
    def results(self):
        return list(self._results)

    def _clear(self):
        self._results.clear()

    def _store(self, result):
        if not isinstance(result, OptimizationResult):
            raise TypeError(
                "Evaluator must return an OptimizationResult."
            )

        self._results.append(result)

    def best_result(self):
        if not self._results:
            return None

        return max(self._results, key=lambda r: r.score)