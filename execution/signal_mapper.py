"""
Signal Mapper.

Maps strategy signals to broker order sides.
"""

from __future__ import annotations

from typing import ClassVar

from shared.enums import (
    OrderSide,
    Signal,
)


class SignalMapper:
    _MAP: ClassVar[dict] = {
        Signal.BUY_CE: OrderSide.BUY,
        Signal.BUY_PE: OrderSide.BUY,
    }

    @classmethod
    def to_order_side(
        cls,
        signal: Signal,
    ) -> OrderSide:
        try:
            return cls._MAP[signal]
        except KeyError as exc:
            raise ValueError(f"Unsupported signal: {signal}") from exc
