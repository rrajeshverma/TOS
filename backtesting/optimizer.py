class Optimizer:
    def __init__(self, parameter_grid, evaluator):
        self.parameter_grid = parameter_grid
        self.evaluator = evaluator

    def optimize(self):
        best_params = None
        best_score = None

        for params in self.parameter_grid.generate():
            score = self.evaluator(params)

            if best_score is None or score > best_score:
                best_score = score
                best_params = params

        return {
            "parameters": best_params,
            "score": best_score,
        }