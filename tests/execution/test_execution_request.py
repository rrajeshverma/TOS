import pytest

from execution.execution_request import ExecutionRequest


def test_create_execution_request():
    request = ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )

    assert request.symbol == "NIFTY"
    assert request.side == "BUY"
    assert request.quantity == 65


def test_invalid_quantity():
    with pytest.raises(ValueError):
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=0,
        )


def test_invalid_side():
    with pytest.raises(ValueError):
        ExecutionRequest(
            symbol="NIFTY",
            side="HOLD",
            quantity=65,
        )
