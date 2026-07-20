from backtesting.optimizer import Optimizer
from backtesting.parameter_grid import ParameterGrid


def test_optimizer_returns_best_parameters():
    grid = ParameterGrid(
        {
            "ema": [20, 50],
            "rsi": [14, 21],
        }
    )

    def evaluator(params):
        if params["ema"] == 50 and params["rsi"] == 21:
            return 100

        return 50

    optimizer = Optimizer(grid, evaluator)

    result = optimizer.optimize()

    assert result["parameters"] == {
        "ema": 50,
        "rsi": 21,
    }

    assert result["score"] == 100
