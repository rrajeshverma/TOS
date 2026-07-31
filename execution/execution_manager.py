"""
=========================================================
Trading Operating System (TOS)

Module      : Execution Manager
Description : Coordinates execution request creation
              and order submission.
=========================================================
"""

from __future__ import annotations

from domain.risk import Risk
from execution.execution_context_factory import (
    ExecutionContextFactory,
)
from execution.execution_request_factory import (
    ExecutionRequestFactory,
)


class ExecutionManager:
    """
    Coordinates the execution pipeline.
    """

    def __init__(
        self,
        execution_engine,
    ) -> None:
        if execution_engine is None:
            raise ValueError("Execution engine cannot be None")

        self._execution_engine = execution_engine

    def execute(
        self,
        risk: Risk,
    ):
        if risk is None:
            raise ValueError("Risk cannot be None")

        if not risk.is_approved:
            return risk

        context = ExecutionContextFactory.create(
            risk,
        )

        request = ExecutionRequestFactory.create(
            context,
        )

        return self._execution_engine.execute(
            request,
        )
