from analytics.benchmark import Benchmark


def test_outperformed():
    benchmark = Benchmark()

    assert benchmark.outperformed(
        strategy_return=18.0,
        benchmark_return=12.0,
    )


def test_not_outperformed():
    benchmark = Benchmark()

    assert not benchmark.outperformed(
        strategy_return=10.0,
        benchmark_return=15.0,
    )


def test_excess_return():
    benchmark = Benchmark()

    assert benchmark.excess_return(
        strategy_return=18.0,
        benchmark_return=12.0,
    ) == 6.0


def test_equal_return():
    benchmark = Benchmark()

    assert benchmark.excess_return(
        strategy_return=15.0,
        benchmark_return=15.0,
    ) == 0.0