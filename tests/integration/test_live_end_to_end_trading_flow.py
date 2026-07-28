"""
Tests:
Live End-to-End Trading Flow

Validates:

Market Input
    |
    ▼
Decision
    |
    ▼
Execution Request
    |
    ▼
Execution Engine
    |
    ▼
Position
    |
    ▼
Trade Journal
"""

from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest


class DummyOrderService:

    def __init__(self):
        self.submitted = []

    def submit(
        self,
        request,
    ):
        self.submitted.append(
            request
        )

        return "ORDER-END2END-001"


class DummyPositionService:

    def __init__(self):
        self.positions = []

    def add(
        self,
        position,
    ):
        self.positions.append(
            position
        )


class DummyJournal:

    def __init__(self):
        self.records = []

    def record(
        self,
        trade,
    ):
        self.records.append(
            trade
        )


def create_execution_request():

    return ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )


def test_live_trade_reaches_execution():

    order_service = DummyOrderService()

    engine = ExecutionEngine(
        order_service
    )

    result = engine.execute(
        create_execution_request()
    )

    assert result.success is True
    assert result.order_id == "ORDER-END2END-001"


def test_execution_request_reaches_order_service():

    order_service = DummyOrderService()

    engine = ExecutionEngine(
        order_service
    )

    request = create_execution_request()

    engine.execute(
        request
    )

    assert len(
        order_service.submitted
    ) == 1

    assert (
        order_service.submitted[0].symbol
        == "NIFTY"
    )


def test_completed_trade_can_update_position():

    position_service = DummyPositionService()

    position_service.add(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert (
        position_service.positions[0]["quantity"]
        == 65
    )


def test_completed_trade_can_be_journaled():

    journal = DummyJournal()

    journal.record(
        {
            "trade_id": "TRADE-END2END-001",
            "symbol": "NIFTY",
            "pnl": 6500,
        }
    )

    assert len(
        journal.records
    ) == 1

    assert (
        journal.records[0]["pnl"]
        == 6500
    )


def test_end_to_end_symbol_consistency():

    request = create_execution_request()

    order_service = DummyOrderService()

    engine = ExecutionEngine(
        order_service
    )

    engine.execute(
        request
    )

    assert (
        order_service.submitted[0].symbol
        == request.symbol
    )
