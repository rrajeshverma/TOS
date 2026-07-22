from execution.execution_result import ExecutionResult


class ExecutionResultMapper:
    """
    Converts broker responses into ExecutionResult.
    """

    def map(
        self,
        response: dict,
    ) -> ExecutionResult:

        if response.get("status") == "success":

            data = response.get(
                "data",
                {},
            )

            return ExecutionResult(
                success=True,
                order_id=data.get(
                    "orderId"
                ),
            )

        return ExecutionResult(
            success=False,
            error=response.get(
                "message",
                "Unknown execution error",
            ),
        )