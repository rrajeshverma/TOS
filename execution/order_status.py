from dataclasses import dataclass


@dataclass
class OrderStatus:
    state: str = "NEW"

    TERMINAL_STATES = (
        "FILLED",
        "CANCELLED",
        "REJECTED",
    )

    def _transition(
        self,
        new_state: str,
    ):
        if self.state in self.TERMINAL_STATES:
            raise ValueError(f"Invalid transition from {self.state}")

        self.state = new_state

    def mark_submitted(self):
        self._transition("SUBMITTED")

    def mark_filled(self):
        self._transition("FILLED")

    def mark_cancelled(self):
        self._transition("CANCELLED")

    def mark_rejected(self):
        self._transition("REJECTED")

    def is_open(self):
        return self.state in (
            "NEW",
            "SUBMITTED",
        )

    def is_closed(self):
        return self.state == "FILLED"

    def is_cancelled(self):
        return self.state == "CANCELLED"

    def is_rejected(self):
        return self.state == "REJECTED"

    def reset(self):
        self.state = "NEW"

    def to_dict(self):
        return {"state": self.state}

    def __str__(self):
        return self.state

    def __repr__(self):
        return f"OrderStatus(state='{self.state}')"
