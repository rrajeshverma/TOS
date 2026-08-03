"""
Order Submitted Event.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderSubmittedEvent:
    """Order submitted."""

    order_id: str
