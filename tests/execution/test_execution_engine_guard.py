from trading.execution_mode import (
    ExecutionMode,
    ExecutionModeGuard,
)

from execution.execution_engine import ExecutionEngine


class DummyOrderService:

    def __init__(self):
        self.called = False


    def submit(
        self,
        request,
    ):

        self.called = True

        return "ORDER001"



def test_live_execution_blocked_without_permission():

    service = DummyOrderService()

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    engine = ExecutionEngine(
        service,
        guard,
    )


    result = engine.execute(
        "TEST_REQUEST"
    )


    assert result.success is False
    assert (
        result.error
        == "Execution blocked by safety guard"
    )


    assert service.called is False



def test_live_execution_allowed_after_enable():

    service = DummyOrderService()

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    guard.enable_live_trading()


    engine = ExecutionEngine(
        service,
        guard,
    )


    result = engine.execute(
        "TEST_REQUEST"
    )


    assert result.success is True
    assert service.called is True



def test_paper_mode_allows_execution():

    service = DummyOrderService()

    guard = ExecutionModeGuard(
        ExecutionMode.PAPER
    )


    engine = ExecutionEngine(
        service,
        guard,
    )


    result = engine.execute(
        "TEST_REQUEST"
    )


    assert result.success is True
