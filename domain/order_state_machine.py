from typing import ClassVar

from domain.order_state import OrderState


class OrderStateMachine:
    _TRANSITIONS: ClassVar[dict] = {
        OrderState.NEW: {
            OrderState.SUBMITTED,
        },
        OrderState.SUBMITTED: {
            OrderState.ACKNOWLEDGED,
            OrderState.REJECTED,
            OrderState.EXPIRED,
        },
        OrderState.ACKNOWLEDGED: {
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.CANCELLED,
        },
        OrderState.PARTIALLY_FILLED: {
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.CANCELLED,
        },
        OrderState.FILLED: set(),
        OrderState.CANCELLED: set(),
        OrderState.REJECTED: set(),
        OrderState.EXPIRED: set(),
    }

    def __init__(self):
        self.state = OrderState.NEW

    def transition(self, new_state: OrderState):
        allowed = self._TRANSITIONS[self.state]

        if new_state not in allowed:
            raise ValueError(f"Invalid transition: {self.state.value} -> {new_state.value}")

        self.state = new_state
        return self.state
