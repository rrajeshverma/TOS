from portfolio.allocation import AllocationEngine


def test_allocation_engine_can_be_created():
    engine = AllocationEngine()

    assert engine is not None


def test_allocates_capital_to_strategy():
    engine = AllocationEngine()

    result = engine.allocate(
        capital=100000,
        allocations={
            "NIFTY_ORB": 50,
        },
    )

    assert result["NIFTY_ORB"] == 50000


def test_allocates_multiple_strategies():
    engine = AllocationEngine()

    result = engine.allocate(
        capital=100000,
        allocations={
            "NIFTY_ORB": 50,
            "BANKNIFTY_ORB": 30,
        },
    )

    assert result["NIFTY_ORB"] == 50000

    assert result["BANKNIFTY_ORB"] == 30000


def test_calculates_remaining_cash():
    engine = AllocationEngine()

    result = engine.allocate(
        capital=100000,
        allocations={
            "NIFTY_ORB": 60,
        },
    )

    assert result["cash_reserve"] == 40000


def test_rejects_allocation_above_100_percent():
    engine = AllocationEngine()

    try:
        engine.allocate(
            capital=100000,
            allocations={
                "NIFTY_ORB": 120,
            },
        )

        assert False

    except ValueError:
        assert True


def test_rejects_negative_capital():
    engine = AllocationEngine()

    try:
        engine.allocate(
            capital=-100,
            allocations={},
        )

        assert False

    except ValueError:
        assert True
