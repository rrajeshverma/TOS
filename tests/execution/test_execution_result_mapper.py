from execution.execution_result_mapper import (
    ExecutionResultMapper,
)
from execution.execution_result import ExecutionResult


def test_map_successful_broker_response():

    mapper = ExecutionResultMapper()

    response = {
        "status": "success",
        "data": {
            "orderId": "ORD123"
        }
    }

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