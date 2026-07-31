"""
Live execution engine.
"""

from __future__ import annotations

from execution.execution_engine import ExecutionEngine


class LiveExecutionEngine(ExecutionEngine):
    """
    Executes orders through the configured live OrderService.

    No behavior is overridden yet—the base ExecutionEngine
    already contains the required orchestration.
    """

    pass
