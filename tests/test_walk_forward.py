from backtesting.walk_forward import WalkForward


def test_walk_forward_runs_all_datasets():
    datasets = [
        [1, 2, 3],
        [4, 5],
        [6],
    ]

    def evaluator(dataset):
        return len(dataset)

    walk_forward = WalkForward(datasets, evaluator)

    assert walk_forward.run() == [3, 2, 1]
