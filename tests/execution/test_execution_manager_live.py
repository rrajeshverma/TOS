from unittest.mock import Mock, patch

from execution.execution_manager import ExecutionManager


def test_execute_creates_request_and_executes():
    engine = Mock()
    manager = ExecutionManager(engine)

    risk = Mock()
    risk.is_approved = True

    context = Mock()
    request = Mock()

    with (
        patch(
            "execution.execution_manager.ExecutionContextFactory.create",
            return_value=context,
        ) as create_context,
        patch(
            "execution.execution_manager.ExecutionRequestFactory.create",
            return_value=request,
        ) as create_request,
    ):
        manager.execute(risk)

    create_context.assert_called_once_with(risk)
    create_request.assert_called_once_with(context)
    engine.execute.assert_called_once_with(request)
