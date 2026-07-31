from unittest.mock import Mock

from execution.paper_execution_engine import PaperExecutionEngine


def test_paper_engine_returns_paper_order():
    order_service = Mock()
    order_service.submit.return_value = "ORDER-1"
    order_service.register_broker_order = Mock()
    order_service.update_status = Mock()

    engine = PaperExecutionEngine(order_service)

    result = engine.execute(Mock())

    assert result.success is True

    order_service.register_broker_order.assert_called_once_with(
        "ORDER-1",
        "PAPER-ORDER",
    )


def test_paper_engine_registers_paper_order_id():
    order_service = Mock()
    order_service.submit.return_value = "ORDER-1"

    engine = PaperExecutionEngine(order_service)

    engine.execute(Mock())

    order_service.register_broker_order.assert_called_once_with(
        "ORDER-1",
        "PAPER-ORDER",
    )


def test_paper_engine_marks_order_submitted():
    order_service = Mock()
    order_service.submit.return_value = "ORDER-1"

    engine = PaperExecutionEngine(order_service)

    engine.execute(Mock())

    order_service.update_status.assert_called_once_with(
        "ORDER-1",
        "SUBMITTED",
    )


def test_paper_engine_returns_execution_result():
    order_service = Mock()
    order_service.submit.return_value = "ORDER-1"

    engine = PaperExecutionEngine(order_service)

    result = engine.execute(Mock())

    assert result.success is True
    assert result.order_id == "ORDER-1"
    assert result.error is None
