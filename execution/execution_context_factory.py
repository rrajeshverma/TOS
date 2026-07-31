"""
Execution Context Factory.

Creates execution contexts from approved Risk objects.
"""

from __future__ import annotations

from domain.risk import Risk
from execution.execution_context import ExecutionContext


class ExecutionContextFactory:
    """Creates ExecutionContext objects."""

    DEFAULT_QUANTITY = 1

    @classmethod
    def create(
        cls,
        risk: Risk,
    ) -> ExecutionContext:
        if risk is None:
            raise ValueError("Risk cannot be None")

        return ExecutionContext(
            risk=risk,
            quantity=cls.DEFAULT_QUANTITY,
        )