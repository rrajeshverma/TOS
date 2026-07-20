from validation.monte_carlo import MonteCarlo


def test_empty_trades():
    mc = MonteCarlo()

    assert mc.run([]) == []


def test_single_trade():
    mc = MonteCarlo(seed=42)

    results = mc.run([100])

    assert len(results) == 1


def test_simulation_count():
    mc = MonteCarlo(
        simulations=100,
        seed=42,
    )

    results = mc.run([1, 2, 3, 4])

    assert len(results) == 100


def test_reproducible_seed():
    trades = [1, -1, 2, -2]

    mc1 = MonteCarlo(
        simulations=20,
        seed=42,
    )

    mc2 = MonteCarlo(
        simulations=20,
        seed=42,
    )

    assert mc1.run(trades) == mc2.run(trades)


def test_results_are_numeric():
    mc = MonteCarlo(
        simulations=20,
        seed=42,
    )

    results = mc.run([1, 2, -1])

    assert all(isinstance(x, (int, float)) for x in results)


def test_zero_simulations():
    mc = MonteCarlo(simulations=0)

    assert mc.run([1, 2, 3]) == []


def test_shuffle_preserves_total_profit():
    trades = [10, -5, 20, -15]

    mc = MonteCarlo(
        simulations=10,
        seed=42,
    )

    results = mc.run(trades)

    assert all(result == 10 for result in results)


def test_zero_simulations():
    mc = MonteCarlo(simulations=0)

    assert mc.run([1, 2, 3]) == []


def test_single_trade():
    mc = MonteCarlo(
        simulations=1,
        seed=42,
    )

    results = mc.run([100])

    assert results == [100]
