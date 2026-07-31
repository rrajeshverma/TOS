from types import SimpleNamespace
from unittest.mock import Mock

from execution.order_events import OrderEventType
from services.execution_service import ExecutionService


def create_service():
    approval_engine = Mock()
    execution_engine = Mock()
    execution_tracker = Mock()
    dispatcher = Mock()

    service = ExecutionService(
        approval_engine=approval_engine,
        execution_engine=execution_engine,
        execution_tracker=execution_tracker,
        event_dispatcher=dispatcher,
    )

    return (
        service,
        approval_engine,
        execution_engine,
        execution_tracker,
        dispatcher,
    )


def approved():
    return SimpleNamespace(
        approved=True,
    )


def rejected():
    return SimpleNamespace(
        approved=False,
    )


def execution_result(
    success=True,
    order_id="ORDER-1",
):
    return SimpleNamespace(
        success=success,
        order_id=order_id,
    )


def test_approval_engine_called():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()
    execution_engine.execute.return_value = execution_result()

    request = object()

    service.execute(request)

    approval_engine.approve.assert_called_once_with(
        request,
        None,
    )


def test_execution_engine_called_after_approval():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()
    execution_engine.execute.return_value = execution_result()

    request = object()

    service.execute(request)

    execution_engine.execute.assert_called_once_with(
        request,
    )


def test_rejected_trade_not_executed():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval = rejected()

    approval_engine.approve.return_value = approval

    result = service.execute(object())

    assert result is approval

    execution_engine.execute.assert_not_called()


def test_failed_execution_not_tracked():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    execution_engine.execute.return_value = execution_result(
        success=False,
    )

    service.execute(object())

    tracker.create.assert_not_called()
    tracker.submit.assert_not_called()


def test_failed_execution_not_published():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    execution_engine.execute.return_value = execution_result(
        success=False,
    )

    service.execute(object())

    dispatcher.publish.assert_not_called()


def test_successful_execution_creates_tracker():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    execution_engine.execute.return_value = execution_result(
        order_id="ABC123",
    )

    service.execute(object())

    tracker.create.assert_called_once_with(
        "ABC123",
    )


def test_successful_execution_submits_tracker():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    execution_engine.execute.return_value = execution_result(
        order_id="ABC123",
    )

    service.execute(object())

    tracker.submit.assert_called_once_with(
        "ABC123",
    )


def test_successful_execution_publishes_event():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    execution_engine.execute.return_value = execution_result(
        order_id="XYZ",
    )

    service.execute(object())

    dispatcher.publish.assert_called_once()

    event = dispatcher.publish.call_args.args[0]

    assert event.order_id == "XYZ"
    assert event.event_type == OrderEventType.SUBMITTED


def test_execute_returns_execution_result():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    result = execution_result()

    execution_engine.execute.return_value = result

    returned = service.execute(object())

    assert returned is result


def test_risk_decision_forwarded():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()
    execution_engine.execute.return_value = execution_result()

    request = object()
    risk = object()

    service.execute(
        request,
        risk,
    )

    approval_engine.approve.assert_called_once_with(
        request,
        risk,
    )


def test_tracker_create_called_before_submit():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()
    execution_engine.execute.return_value = execution_result(
        order_id="ORDER-100",
    )

    service.execute(object())

    assert tracker.method_calls == [
        ("create", ("ORDER-100",), {}),
        ("submit", ("ORDER-100",), {}),
    ]


def test_execution_engine_not_called_when_rejected():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = rejected()

    service.execute(object())

    execution_engine.execute.assert_not_called()


def test_tracker_not_updated_when_rejected():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = rejected()

    service.execute(object())

    tracker.create.assert_not_called()
    tracker.submit.assert_not_called()


def test_dispatcher_not_called_when_rejected():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = rejected()

    service.execute(object())

    dispatcher.publish.assert_not_called()


def test_execution_result_without_success_attribute_returns_directly():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()

    result = SimpleNamespace(
        order_id="ORDER-1",
    )

    execution_engine.execute.return_value = result

    returned = service.execute(object())

    assert returned is result

    tracker.create.assert_not_called()
    tracker.submit.assert_not_called()
    dispatcher.publish.assert_not_called()


def test_published_event_contains_correct_order_id():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()
    execution_engine.execute.return_value = execution_result(
        order_id="MY-ORDER",
    )

    service.execute(object())

    event = dispatcher.publish.call_args.args[0]

    assert event.order_id == "MY-ORDER"


def test_execute_returns_rejection_object():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval = rejected()

    approval_engine.approve.return_value = approval

    returned = service.execute(object())

    assert returned is approval


def test_execution_called_only_once():
    (
        service,
        approval_engine,
        execution_engine,
        tracker,
        dispatcher,
    ) = create_service()

    approval_engine.approve.return_value = approved()
    execution_engine.execute.return_value = execution_result()

    service.execute(object())

    assert execution_engine.execute.call_count == 1
