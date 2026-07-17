from backtesting.parameter_grid import ParameterGrid


def test_parameter_grid_generates_all_combinations():
    grid = ParameterGrid(
        {
            "ema": [20, 50],
            "rsi": [14, 21],
        }
    )

    combinations = list(grid.generate())

    expected = [
        {"ema": 20, "rsi": 14},
        {"ema": 20, "rsi": 21},
        {"ema": 50, "rsi": 14},
        {"ema": 50, "rsi": 21},
    ]

    assert combinations == expected