import random

from optimizer.optimization_result import OptimizationResult


class RandomSearch:
    def __init__(self, parameter_space, sample_size, seed=None):
        self._parameter_space = parameter_space
        self._sample_size = max(0, sample_size)
        self._random = random.Random(seed)
        self._results = []

    @property
    def results(self):
        return list(self._results)

    def run(self, evaluator):
        self._results.clear()

        combinations = list(self._parameter_space.generate())

        if not combinations or self._sample_size == 0:
            return []

        sample_size = min(self._sample_size, len(combinations))

        sampled = self._random.sample(combinations, sample_size)

        for params in sampled:
            result = evaluator(params)

            if not isinstance(result, OptimizationResult):
                raise TypeError("Evaluator must return an OptimizationResult.")

            self._results.append(result)

        return self.results

    def best_result(self):
        if not self._results:
            return None

        return max(self._results, key=lambda r: r.score)
