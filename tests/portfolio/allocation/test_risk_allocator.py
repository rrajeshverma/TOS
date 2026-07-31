from portfolio.allocation.risk_allocator import RiskAllocator


def test_max_strategy_risk():
    allocator = RiskAllocator(10000)

    allocator.allocate_risk("NIFTY", 2000)

    assert allocator.max_strategy_risk("NIFTY") == 2000


def test_total_portfolio_risk():
    allocator = RiskAllocator(10000)

    allocator.allocate_risk("A", 2000)
    allocator.allocate_risk("B", 3000)

    assert allocator.total_allocated_risk() == 5000


def test_remaining_risk():
    allocator = RiskAllocator(10000)

    allocator.allocate_risk("A", 3000)

    assert allocator.remaining_risk() == 7000


def test_risk_limit():
    allocator = RiskAllocator(10000)

    result = allocator.allocate_risk(
        "A",
        15000,
    )

    assert result == 10000


def test_negative_risk():
    allocator = RiskAllocator(10000)

    assert allocator.allocate_risk("A", -500) == 0


def test_daily_loss_distribution():
    allocator = RiskAllocator(10000)

    allocator.distribute_daily_loss(500)

    assert allocator.daily_loss == 500


def test_margin_validation_true():
    allocator = RiskAllocator(10000)

    assert allocator.validate_margin(5000)


def test_margin_validation_false():
    allocator = RiskAllocator(10000)

    allocator.allocate_risk("A", 8000)

    assert not allocator.validate_margin(5000)


def test_summary():
    allocator = RiskAllocator(10000)

    allocator.allocate_risk("A", 2000)

    summary = allocator.summary()

    assert summary["allocated_risk"] == 2000


def test_multiple_strategies():
    allocator = RiskAllocator(10000)

    allocator.allocate_risk("A", 1000)
    allocator.allocate_risk("B", 2000)

    summary = allocator.summary()

    assert summary["strategies"] == 2
