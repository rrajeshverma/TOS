from portfolio.allocation.allocation_engine import AllocationEngine


def test_initialize_engine():
    engine = AllocationEngine(100000)

    assert engine.capital == 100000


def test_allocate_capital():

    engine = AllocationEngine(100000)

    result = engine.allocate(
        "NIFTY",
        20000,
    )

    assert result == 20000


def test_get_allocation():

    engine = AllocationEngine(100000)

    engine.allocate("NIFTY", 20000)

    assert engine.get_allocation("NIFTY") == 20000


def test_total_allocated():

    engine = AllocationEngine(100000)

    engine.allocate("NIFTY", 20000)
    engine.allocate("BANKNIFTY", 30000)

    assert engine.total_allocated() == 50000


def test_remaining_capital():

    engine = AllocationEngine(100000)

    engine.allocate("NIFTY", 25000)

    assert engine.remaining_capital() == 75000


def test_allocation_limit():

    engine = AllocationEngine(100000)

    result = engine.allocate(
        "NIFTY",
        150000,
    )

    assert result == 100000


def test_negative_allocation():

    engine = AllocationEngine(100000)

    result = engine.allocate(
        "NIFTY",
        -500,
    )

    assert result == 0


def test_multiple_strategies():

    engine = AllocationEngine(100000)

    engine.allocate("A", 10000)
    engine.allocate("B", 20000)

    assert len(engine.allocations) == 2


def test_remove_allocation():

    engine = AllocationEngine(100000)

    engine.allocate("A", 10000)

    engine.remove_allocation("A")

    assert engine.total_allocated() == 0


def test_summary():

    engine = AllocationEngine(100000)

    engine.allocate("A", 25000)

    summary = engine.summary()

    assert summary["allocated"] == 25000
    assert summary["remaining"] == 75000
