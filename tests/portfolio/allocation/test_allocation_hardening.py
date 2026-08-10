from portfolio.allocation.allocation_engine import AllocationEngine
from portfolio.allocation.rebalance_manager import RebalanceManager
from portfolio.allocation.risk_allocator import RiskAllocator

# -------------------------
# Allocation Engine
# -------------------------


def test_allocation_initial_capital():
    engine = AllocationEngine(100000)

    assert engine.capital == 100000


def test_allocate_strategy():
    engine = AllocationEngine(100000)

    result = engine.allocate(
        "NIFTY",
        20000,
    )

    assert result == 20000


def test_negative_allocation_becomes_zero():
    engine = AllocationEngine(100000)

    result = engine.allocate(
        "NIFTY",
        -100,
    )

    assert result == 0


def test_allocation_cannot_exceed_capital():
    engine = AllocationEngine(100000)

    result = engine.allocate(
        "NIFTY",
        200000,
    )

    assert result == 100000


def test_remaining_capital():
    engine = AllocationEngine(100000)

    engine.allocate(
        "NIFTY",
        30000,
    )

    assert engine.remaining_capital() == 70000


def test_total_allocated():
    engine = AllocationEngine(100000)

    engine.allocate(
        "NIFTY",
        30000,
    )

    assert engine.total_allocated() == 30000


def test_multiple_strategy_allocation():
    engine = AllocationEngine(100000)

    engine.allocate("A", 20000)
    engine.allocate("B", 30000)

    assert engine.total_allocated() == 50000


def test_get_strategy_allocation():
    engine = AllocationEngine(100000)

    engine.allocate("A", 10000)

    assert engine.get_allocation("A") == 10000


def test_remove_strategy_allocation():
    engine = AllocationEngine(100000)

    engine.allocate("A", 10000)

    engine.remove_allocation("A")

    assert engine.get_allocation("A") == 0


# -------------------------
# Rebalance Manager
# -------------------------


def test_should_rebalance_true():
    manager = RebalanceManager(threshold=10)

    assert manager.should_rebalance(
        100,
        120,
    )


def test_should_rebalance_false():
    manager = RebalanceManager(threshold=10)

    assert not manager.should_rebalance(
        100,
        105,
    )


def test_rebalance_creates_event():
    manager = RebalanceManager()

    event = manager.rebalance(
        100,
        120,
    )

    assert event["from"] == 100


def test_rebalance_history():
    manager = RebalanceManager()

    manager.rebalance(
        100,
        120,
    )

    assert manager.rebalance_count() == 1


def test_last_rebalance():
    manager = RebalanceManager()

    manager.rebalance(
        100,
        120,
    )

    assert manager.last_rebalance()["to"] == 120


# -------------------------
# Risk Allocator
# -------------------------


def test_risk_allocation():
    risk = RiskAllocator(10000)

    assert (
        risk.allocate_risk(
            "NIFTY",
            2000,
        )
        == 2000
    )


def test_negative_risk_zero():
    risk = RiskAllocator(10000)

    assert (
        risk.allocate_risk(
            "NIFTY",
            -100,
        )
        == 0
    )


def test_remaining_risk():
    risk = RiskAllocator(10000)

    risk.allocate_risk(
        "NIFTY",
        2000,
    )

    assert risk.remaining_risk() == 8000


def test_margin_validation():
    risk = RiskAllocator(10000)

    assert risk.validate_margin(5000)


def test_daily_loss_distribution():
    risk = RiskAllocator(10000)

    risk.distribute_daily_loss(500)

    assert risk.daily_loss == 500


def test_risk_summary():
    risk = RiskAllocator(10000)

    result = risk.summary()

    assert result["total_risk"] == 10000
