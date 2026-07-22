from optimizer.grid_search import GridSearch
from optimizer.optimization_result import OptimizationResult
from optimizer.parameter_space import ParameterSpace


def test_empty_parameter_space():
    space = ParameterSpace()

    search = GridSearch(space)

    results = search.run(lambda params: OptimizationResult(parameters=params))

    assert results == []


def test_single_parameter():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = GridSearch(space)

    results = search.run(lambda params: OptimizationResult(parameters=params))

    assert len(results) == 2


def test_multiple_parameters():
    space = ParameterSpace()

    space.add("ema", [20, 30])
    space.add("rsi", [50, 60])

    search = GridSearch(space)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert len(results) == 4


def test_results_property():
    space = ParameterSpace()

    space.add("ema", [20])

    search = GridSearch(space)

    search.run(lambda p: OptimizationResult(parameters=p))

    assert len(search.results) == 1


def test_best_result():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = GridSearch(space)

    def evaluator(params):
        return OptimizationResult(parameters=params, net_profit=params["ema"])

    search.run(evaluator)

    assert search.best_result().net_profit == 30


def test_best_result_empty():
    space = ParameterSpace()

    search = GridSearch(space)

    assert search.best_result() is None


def test_evaluator_called_every_time():
    counter = 0

    def evaluator(params):
        nonlocal counter
        counter += 1
        return OptimizationResult(parameters=params)

    space = ParameterSpace()

    space.add("ema", [20, 30])
    space.add("rsi", [40, 50])

    GridSearch(space).run(evaluator)

    assert counter == 4


def test_generation_order():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    search = GridSearch(space)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert results[0].parameters["ema"] == 20
    assert results[1].parameters["ema"] == 30


import pytest


def test_evaluator_exception():
    space = ParameterSpace()

    space.add("ema", [20])

    def evaluator(params):
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        GridSearch(space).run(evaluator)


def test_result_count():
    space = ParameterSpace()

    space.add("ema", [20, 30, 40])
    space.add("rsi", [45, 55])

    search = GridSearch(space)

    results = search.run(lambda p: OptimizationResult(parameters=p))

    assert len(results) == space.count()


def test_store_invalid_result_raises_type_error():
    space = ParameterSpace()

    search = GridSearch(space)

    with pytest.raises(
        TypeError,
        match="Evaluator must return an OptimizationResult.",
    ):
        search._store(object())


def test_evaluator_returns_invalid_result():
    space = ParameterSpace()
    space.add("ema", [20])

    search = GridSearch(space)

    def evaluator(params):
        return object()  # Not an OptimizationResult

    with pytest.raises(
        TypeError,
        match="Evaluator must return an OptimizationResult.",
    ):
        search.run(evaluator)
