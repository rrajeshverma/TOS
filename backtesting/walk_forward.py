class WalkForward:
    def __init__(self, datasets, evaluator):
        self.datasets = datasets
        self.evaluator = evaluator

    def run(self):
        results = []

        for dataset in self.datasets:
            results.append(self.evaluator(dataset))

        return results