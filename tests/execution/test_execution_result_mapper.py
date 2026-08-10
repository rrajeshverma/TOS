from execution.execution_result import ExecutionResult
from execution.execution_result_mapper import (
    ExecutionResultMapper,
)


def test_map_successful_broker_response():
    mapper = ExecutionResultMapper()

    response = {"status": "success", "data": {"orderId": "ORD123"}}

    result = mapper.map(response)

    assert isinstance(
        result,
        ExecutionResult,
    )

    assert result.success is True
    assert result.order_id == "ORD123"


def test_map_failed_broker_response():
    mapper = ExecutionResultMapper()

    response = {
        "status": "failed",
        "message": "Insufficient funds",
    }

    result = mapper.map(response)

    assert result.success is False
    assert result.error == "Insufficient funds"


def test_map_success_without_data():
    mapper = ExecutionResultMapper()

    result = mapper.map({"status": "success"})

    assert result.success is True
    assert result.order_id is None


def test_map_failure_without_message():
    mapper = ExecutionResultMapper()

    result = mapper.map({"status": "failed"})

    assert result.success is False
    assert result.error == "Unknown execution error"


def test_map_failure_with_message():
    mapper = ExecutionResultMapper()

    result = mapper.map(
        {
            "status": "failed",
            "message": "Rejected",
        }
    )

    assert result.success is False
    assert result.error == "Rejected"
