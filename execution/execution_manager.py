"""
Execution Manager.

Coordinates the execution pipeline.
"""

from __future__ import annotations

from domain.instrument import Instrument
from domain.risk import Risk
from execution.execution_context_factory import ExecutionContextFactory
from execution.execution_request_factory import ExecutionRequestFactory


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
        quantity: int | None = None,
        instrument: Instrument | None = None,
    ):
        if risk is None:
            raise ValueError("Risk cannot be None")

        if not risk.is_approved:
            return risk

        # Preserve the original execution path exactly when
        # no optional execution parameters are supplied.
        if quantity is None and instrument is None:
            context = ExecutionContextFactory.create(
                risk,
            )
        else:
            context = ExecutionContextFactory.create(
                risk,
                quantity=quantity,
                instrument=instrument,
            )

        request = ExecutionRequestFactory.create(
            context,
        )

        return self._execution_engine.execute(
            request,
        )
