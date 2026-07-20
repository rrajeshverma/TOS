from optimizer.random_search import RandomSearch
from optimizer.parameter_space import ParameterSpace
from optimizer.optimization_result import OptimizationResult


def test_empty_parameter_space():
    space = ParameterSpace()

    search = RandomSearch(space, sample_size=5)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert results == []


def test_zero_sample_size():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = RandomSearch(space, sample_size=0)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert results == []


def test_sample_one():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = RandomSearch(space, sample_size=1, seed=42)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert len(results) == 1


def test_sample_less_than_total():
    space = ParameterSpace()

    space.add("ema", [20, 30, 40])
    space.add("rsi", [45, 55])

    search = RandomSearch(space, sample_size=3, seed=42)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert len(results) == 3


def test_sample_more_than_total():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = RandomSearch(space, sample_size=10)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert len(results) == 2


def test_seed_reproducible():
    space = ParameterSpace()

    space.add("ema", [20, 30, 40])

    search1 = RandomSearch(space, sample_size=2, seed=123)
    search2 = RandomSearch(space, sample_size=2, seed=123)

    r1 = search1.run(lambda p: OptimizationResult(parameters=p))

    r2 = search2.run(lambda p: OptimizationResult(parameters=p))

    assert [x.parameters for x in r1] == [x.parameters for x in r2]


def test_evaluator_called():
    counter = 0

    def evaluator(params):
        nonlocal counter
        counter += 1
        return OptimizationResult(parameters=params)

    space = ParameterSpace()

    space.add("ema", [20, 30, 40])

    RandomSearch(
        space,
        sample_size=2,
        seed=42,
    ).run(evaluator)

    assert counter == 2


def test_best_result():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = RandomSearch(
        space,
        sample_size=2,
        seed=42,
    )

    def evaluator(params):
        return OptimizationResult(parameters=params, net_profit=params["ema"])

    search.run(evaluator)

    assert search.best_result().net_profit == 30


def test_results_property():
    space = ParameterSpace()

    space.add("ema", [20])

    search = RandomSearch(space, sample_size=1)

    search.run(lambda p: OptimizationResult(parameters=p))

    assert len(search.results) == 1


def test_result_type():
    space = ParameterSpace()

    space.add("ema", [20])

    search = RandomSearch(space, sample_size=1)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert isinstance(results[0], OptimizationResult)
