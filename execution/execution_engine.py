from execution.execution_result import ExecutionResult


class ExecutionEngine:

    def __init__(self, order_service):
        self.order_service = order_service

    def execute(self, request):
        if request is None:
            raise ValueError("ExecutionRequest cannot be None")

        try:
            order_id = self.order_service.submit(request)

            return ExecutionResult(
                success=True,
                order_id=order_id,
            )

        except Exception as exc:
            return ExecutionResult(
                success=False,
                error=str(exc),
            )