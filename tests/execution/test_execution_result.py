from execution.execution_result import ExecutionResult


def test_success_result():
    result = ExecutionResult(
        success=True,
        order_id="ORD123",
    )

    assert result.success is True
    assert result.order_id == "ORD123"


def test_failure_result():
    result = ExecutionResult(
        success=False,
        error="Broker unavailable",
    )

    assert result.success is False
    assert result.error == "Broker unavailable"