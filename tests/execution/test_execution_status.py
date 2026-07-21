from execution.execution_status import ExecutionStatus


def test_status_values():
    assert ExecutionStatus.PENDING.value == "PENDING"
    assert ExecutionStatus.SUBMITTED.value == "SUBMITTED"
    assert ExecutionStatus.FILLED.value == "FILLED"
    assert ExecutionStatus.REJECTED.value == "REJECTED"
    assert ExecutionStatus.FAILED.value == "FAILED"