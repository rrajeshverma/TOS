from optimizer.optimization_result import OptimizationResult
from optimizer.strategy_ranker import StrategyRanker


def make_result(**kwargs):
    return OptimizationResult(
        parameters={},
        **kwargs,
    )


def test_empty_ranker():
    ranker = StrategyRanker([])

    assert ranker.best() is None


def test_best_result():
    results = [
        make_result(net_profit=100),
        make_result(net_profit=300),
        make_result(net_profit=200),
    ]

    ranker = StrategyRanker(results)

    assert ranker.best().net_profit == 300


def test_top_n():
    results = [
        make_result(net_profit=100),
        make_result(net_profit=300),
        make_result(net_profit=200),
    ]

    ranker = StrategyRanker(results)

    top = ranker.top(2)

    assert len(top) == 2
    assert top[0].net_profit == 300
    assert top[1].net_profit == 200


def test_profitable():
    results = [
        make_result(net_profit=-100),
        make_result(net_profit=200),
        make_result(net_profit=50),
    ]

    ranker = StrategyRanker(results)

    profitable = ranker.profitable()

    assert len(profitable) == 2


def test_sort_by_profit():
    results = [
        make_result(net_profit=150),
        make_result(net_profit=50),
        make_result(net_profit=300),
    ]

    ranker = StrategyRanker(results)

    ranked = ranker.sort(key=lambda r: r.net_profit)

    assert ranked[0].net_profit == 300


def test_sort_by_sharpe():
    results = [
        make_result(sharpe_ratio=1.1),
        make_result(sharpe_ratio=2.5),
        make_result(sharpe_ratio=0.8),
    ]

    ranker = StrategyRanker(results)

    ranked = ranker.sort(key=lambda r: r.sharpe_ratio)

    assert ranked[0].sharpe_ratio == 2.5


def test_results_property():
    results = [make_result(net_profit=100)]

    ranker = StrategyRanker(results)

    assert len(ranker.results) == 1
