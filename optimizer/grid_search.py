from optimizer.optimization_result import OptimizationResult
from optimizer.base_search import BaseSearch


class GridSearch(BaseSearch):
    def __init__(self, parameter_space):
        super().__init__()
        self._parameter_space = parameter_space

    def run(self, evaluator):
        self._clear()

        for params in self._parameter_space.generate():
            result = evaluator(params)

            if not isinstance(result, OptimizationResult):
                raise TypeError("Evaluator must return an OptimizationResult.")

            self._store(result)

        return self.results
