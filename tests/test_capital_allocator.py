from portfolio.capital_allocator import CapitalAllocator


# ============================================================
# Allocation
# ============================================================

def test_allocate_fixed_amount():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate(10000) == 10000


def test_allocate_zero():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate(0) == 0


def test_allocate_cannot_exceed_capital():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate(150000) == 100000


# ============================================================
# Percentage Allocation
# ============================================================

def test_allocate_percent():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate_percent(10) == 10000


def test_allocate_percent_zero():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate_percent(0) == 0


def test_allocate_percent_full():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate_percent(100) == 100000


# ============================================================
# Reserve Capital
# ============================================================

def test_reserve_capital():
    allocator = CapitalAllocator(100000)

    allocator.reserve(20000)

    assert allocator.reserved == 20000


def test_available_after_reserve():
    allocator = CapitalAllocator(100000)

    allocator.reserve(20000)

    assert allocator.available() == 80000


def test_reserve_never_exceeds_capital():
    allocator = CapitalAllocator(100000)

    allocator.reserve(150000)

    assert allocator.reserved == 100000


# ============================================================
# Release
# ============================================================

def test_release_reserved():
    allocator = CapitalAllocator(100000)

    allocator.reserve(30000)
    allocator.release(10000)

    assert allocator.reserved == 20000


def test_release_all():
    allocator = CapitalAllocator(100000)

    allocator.reserve(30000)
    allocator.release(50000)

    assert allocator.reserved == 0


# ============================================================
# Utilization
# ============================================================

def test_utilization_percent():
    allocator = CapitalAllocator(100000)

    allocator.reserve(25000)

    assert allocator.utilization_percent() == 25.0


def test_utilization_zero():
    allocator = CapitalAllocator(100000)

    assert allocator.utilization_percent() == 0.0


# ============================================================
# Summary
# ============================================================

def test_summary_total():
    allocator = CapitalAllocator(100000)

    summary = allocator.summary()

    assert summary["capital"] == 100000


def test_summary_reserved():
    allocator = CapitalAllocator(100000)

    allocator.reserve(20000)

    summary = allocator.summary()

    assert summary["reserved"] == 20000


def test_summary_available():
    allocator = CapitalAllocator(100000)

    allocator.reserve(20000)

    summary = allocator.summary()

    assert summary["available"] == 80000


def test_summary_utilization():
    allocator = CapitalAllocator(100000)

    allocator.reserve(25000)

    summary = allocator.summary()

    assert summary["utilization_percent"] == 25.0


def test_summary_allocate_percent():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate_percent(5) == 5000


def test_summary_allocate_half():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate_percent(50) == 50000


def test_summary_allocate_quarter():
    allocator = CapitalAllocator(100000)

    assert allocator.allocate_percent(25) == 25000