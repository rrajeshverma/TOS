"""
Integration Test:

Execution Engine + Broker Confirmation

Validates:
- Broker accepted response
- Broker rejection handling
- Missing confirmation handling
- Execution safety after broker response
"""

from execution.broker_confirmation import (
    BrokerConfirmationValidator,
)

from execution.execution_engine import (
    ExecutionEngine,
)

from trading.execution_mode import (
    ExecutionMode,
    ExecutionModeGuard,
)


class DummyOrderService:
    def __init__(
        self,
        response=None,
    ):
        self.response = response
        self.submitted = False

    def submit(
        self,
        request,
    ):
        self.submitted = True

        return "ORDER001"

    def place_order(
        self,
        request,
    ):
        return self.response


def test_broker_success_confirmation():
    validator = BrokerConfirmationValidator()

    response = {
        "status": "success",
        "orderId": "DHAN001",
    }

    assert validator.is_confirmed(response) is True


def test_broker_failure_confirmation():
    validator = BrokerConfirmationValidator()

    response = {
        "status": "failed",
        "orderId": "DHAN001",
    }

    assert validator.is_confirmed(response) is False


def test_execution_engine_receives_broker_confirmation():
    service = DummyOrderService(
        {
            "status": "success",
            "orderId": "DHAN001",
        }
    )

    guard = ExecutionModeGuard(ExecutionMode.PAPER)

    engine = ExecutionEngine(
        service,
        guard,
    )

    result = engine.execute("NIFTY_ORDER")

    assert result.success is True

    assert service.submitted is True


def test_rejected_broker_response_is_not_confirmed():
    service = DummyOrderService(
        {
            "status": "failed",
            "orderId": None,
        }
    )

    validator = BrokerConfirmationValidator()

    assert validator.is_confirmed(service.response) is False


def test_missing_broker_response_is_blocked():
    validator = BrokerConfirmationValidator()

    assert validator.is_confirmed(None) is False


def test_complete_broker_handshake_flow():
    service = DummyOrderService(
        {
            "status": "success",
            "orderId": "DHAN999",
        }
    )

    guard = ExecutionModeGuard(ExecutionMode.PAPER)

    engine = ExecutionEngine(
        service,
        guard,
    )

    result = engine.execute("VALID_ORDER")

    confirmation = BrokerConfirmationValidator().is_confirmed(service.response)

    assert result.success is True

    assert confirmation is True
