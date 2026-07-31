from execution.execution_engine import ExecutionEngine


class PaperExecutionEngine(ExecutionEngine):
    """
    Simulates broker execution for paper trading.
    """

    def _place_order(
        self,
        request,
    ):
        return {
            "orderId": "PAPER-ORDER",
        }
