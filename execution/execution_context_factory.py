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
        quantity: int | None = None,
    ) -> ExecutionContext:
        if risk is None:
            raise ValueError("Risk cannot be None")

        if quantity is not None and quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        return ExecutionContext(
            risk=risk,
            quantity=cls.DEFAULT_QUANTITY if quantity is None else quantity,
        )
