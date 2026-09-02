"""
Execution Request Factory.

Creates broker execution requests from execution contexts.
"""

from __future__ import annotations

from execution.execution_context import ExecutionContext
from execution.execution_request import ExecutionRequest
from execution.signal_mapper import SignalMapper


class ExecutionRequestFactory:
    """Creates ExecutionRequest objects."""

    @staticmethod
    def create(
        context: ExecutionContext,
    ) -> ExecutionRequest:
        if context is None:
            raise ValueError("ExecutionContext cannot be None")

        decision = context.risk.decision
        market = decision.market

        instrument = context.instrument

        if instrument is not None:
            symbol = instrument.symbol
            security_id = instrument.security_id
            exchange_segment = instrument.exchange_segment
        else:
            # Backward-compatible path for existing callers.
            symbol = market.symbol
            security_id = None
            exchange_segment = None

        return ExecutionRequest(
            symbol=symbol,
            side=SignalMapper.to_order_side(
                decision.signal,
            ).value,
            quantity=context.quantity,
            security_id=security_id,
            exchange_segment=exchange_segment,
        )
