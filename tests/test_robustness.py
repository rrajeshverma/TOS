from optimizer.optimization_result import OptimizationResult
from validation.robustness import Robustness


def make_result(**kwargs):
    defaults = {
        "parameters": {},
        "trades": 100,
        "wins": 50,
        "losses": 50,
        "net_profit": 0,
        "max_drawdown": 0,
        "profit_factor": 1.0,
        "expectancy": 0.0,
        "sharpe_ratio": 1.0,
        "sortino_ratio": 1.0,
        "calmar_ratio": 1.0,
    }

    defaults.update(kwargs)

    return OptimizationResult(**defaults)


def test_empty_results():
    robustness = Robustness()

    assert robustness.evaluate([]) == 0.0


def test_single_result():
    result = make_result(net_profit=100)

    robustness = Robustness()

    score = robustness.evaluate([result])

    assert score == 1.0


def test_identical_results():
    results = [
        make_result(net_profit=100),
        make_result(net_profit=100),
        make_result(net_profit=100),
    ]

    robustness = Robustness()

    assert robustness.evaluate(results) == 1.0


def test_variable_results():
    results = [
        make_result(net_profit=100),
        make_result(net_profit=50),
        make_result(net_profit=-100),
    ]

    robustness = Robustness()

    score = robustness.evaluate(results)

    assert 0.0 <= score <= 1.0


def test_more_consistent_scores_higher():
    stable = [
        make_result(net_profit=100),
        make_result(net_profit=95),
        make_result(net_profit=102),
    ]

    unstable = [
        make_result(net_profit=300),
        make_result(net_profit=-200),
        make_result(net_profit=50),
    ]

    robustness = Robustness()

    assert robustness.evaluate(stable) > robustness.evaluate(unstable)

def test_zero_mean_profit_returns_zero():
    results = [
        make_result(net_profit=100),
        make_result(net_profit=-100),
    ]

    robustness = Robustness()

    assert robustness.evaluate(results) == 0.0