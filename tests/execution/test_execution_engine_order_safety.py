"""
Integration Test:

Execution Engine Order Safety

Validates:
- Execution mode protection
- Order validation
- Duplicate order prevention
- Safe submission flow
"""

from execution.execution_engine import ExecutionEngine
from execution.order_duplicate_guard import (
    OrderDuplicateGuard,
)
from execution.order_validator import (
    OrderValidator,
)

from trading.execution_mode import (
    ExecutionMode,
    ExecutionModeGuard,
)


class DummyOrder:
    def __init__(
        self,
        symbol="NIFTY",
        quantity=65,
    ):
        self.symbol = symbol
        self.quantity = quantity


class DummyOrderService:
    def __init__(self):
        self.submitted = []

    def submit(
        self,
        request,
    ):
        self.submitted.append(request)

        return "ORDER001"


def create_engine():
    service = DummyOrderService()

    mode_guard = ExecutionModeGuard(ExecutionMode.PAPER)

    return (
        ExecutionEngine(
            service,
            mode_guard,
        ),
        service,
    )


def test_paper_mode_order_is_allowed():
    engine, service = create_engine()

    result = engine.execute(DummyOrder())

    assert result.success is True

    assert len(service.submitted) == 1


def test_live_mode_without_permission_is_blocked():
    service = DummyOrderService()

    guard = ExecutionModeGuard(ExecutionMode.LIVE)

    engine = ExecutionEngine(
        service,
        guard,
    )

    result = engine.execute(DummyOrder())

    assert result.success is False

    assert len(service.submitted) == 0


def test_live_mode_after_enable_allows_execution():
    service = DummyOrderService()

    guard = ExecutionModeGuard(ExecutionMode.LIVE)

    guard.enable_live_trading()

    engine = ExecutionEngine(
        service,
        guard,
    )

    result = engine.execute(DummyOrder())

    assert result.success is True


def test_invalid_order_is_rejected():
    validator = OrderValidator()

    assert validator.validate(None) is False


def test_duplicate_guard_blocks_repeat_order():
    duplicate_guard = OrderDuplicateGuard()

    key = "NIFTY_BUY_65"

    assert duplicate_guard.can_submit(key) is True

    duplicate_guard.register(key)

    assert duplicate_guard.can_submit(key) is False


def test_complete_order_safety_stack():
    validator = OrderValidator()

    duplicate_guard = OrderDuplicateGuard()

    order = DummyOrder()

    assert validator.validate(order) is True

    key = f"{order.symbol}_{order.quantity}"

    assert duplicate_guard.can_submit(key) is True

    duplicate_guard.register(key)

    assert duplicate_guard.can_submit(key) is False
