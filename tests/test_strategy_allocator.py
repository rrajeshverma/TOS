from portfolio.strategy_allocator import StrategyAllocator


def test_initialize_allocator():
    allocator = StrategyAllocator(100000)

    assert allocator.total_capital == 100000


def test_allocate_strategy_capital():
    allocator = StrategyAllocator(100000)

    result = allocator.allocate(
        "ORB",
        20000,
    )

    assert result == 20000


def test_get_strategy_allocation():
    allocator = StrategyAllocator(100000)

    allocator.allocate("ORB", 20000)

    assert allocator.get_allocation("ORB") == 20000


def test_total_allocated():
    allocator = StrategyAllocator(100000)

    allocator.allocate("A", 10000)
    allocator.allocate("B", 20000)

    assert allocator.total_allocated() == 30000


def test_remaining_capital():
    allocator = StrategyAllocator(100000)

    allocator.allocate("A", 25000)

    assert allocator.remaining_capital() == 75000


def test_allocation_limit():
    allocator = StrategyAllocator(100000)

    result = allocator.allocate(
        "A",
        150000,
    )

    assert result == 100000


def test_negative_allocation():
    allocator = StrategyAllocator(100000)

    assert (
        allocator.allocate(
            "A",
            -500,
        )
        == 0
    )


def test_release_strategy():
    allocator = StrategyAllocator(100000)

    allocator.allocate("A", 20000)

    released = allocator.release("A")

    assert released == 20000


def test_utilization():
    allocator = StrategyAllocator(100000)

    allocator.allocate("A", 25000)

    assert allocator.utilization() == 25.0


def test_summary():
    allocator = StrategyAllocator(100000)

    allocator.allocate("A", 25000)

    summary = allocator.summary()

    assert summary["allocated"] == 25000
    assert summary["strategies"] == 1
